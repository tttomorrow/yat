/* 
 * Copyright (c) 2021 Huawei Technologies Co.,Ltd.
 *
 * openGauss is licensed under Mulan PSL v2.
 * You can use this software according to the terms and conditions of the Mulan PSL v2.
 * You may obtain a copy of Mulan PSL v2 at:
 *
 *           http://license.coscl.org.cn/MulanPSL2
 *        
 * THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
 * EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
 * MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
 * See the Mulan PSL v2 for more details.
 */
 
package com.huawei.gauss.yat.script

import com.huawei.gauss.yat.common.Benchmark
import com.huawei.gauss.yat.common.MacroReplacer
import com.huawei.gauss.yat.common.WorkPool
import com.huawei.gauss.yat.common.commander.CommandResult
import com.huawei.gauss.yat.common.commander.ShellCommander
import com.huawei.gauss.yat.compatible.exception.SqlExceptionCompat
import com.huawei.gauss.yat.convert.ResultConvert
import com.huawei.gauss.yat.setting.ConnectionPool
import com.huawei.gauss.yat.sql.Result
import com.huawei.gauss.yat.sql.parser.*
import com.huawei.gauss.yat.sql.parser.statement.*
import groovy.lang.Binding
import groovy.lang.GroovyShell
import org.apache.commons.codec.binary.Hex
import java.io.BufferedOutputStream
import java.io.File
import java.io.FileOutputStream
import java.io.OutputStream
import java.math.BigDecimal
import java.nio.charset.Charset
import java.sql.*
import java.sql.Date
import java.time.Duration
import java.time.LocalDateTime
import java.util.*
import java.util.concurrent.Future
import java.util.concurrent.locks.ReentrantLock
import kotlin.concurrent.withLock
import kotlin.properties.ReadWriteProperty
import kotlin.reflect.KProperty

abstract class SqlOutput : AutoCloseable {
    abstract fun echoMust(msg: String, lf: Boolean = true)
    abstract fun newWithSuffix(suffix: String): FileSqlOutput

    fun echo(comment: CommentStatement) {
        if (!echoComment) {
            return
        }
        if (comment.multiline) {
            echoMust(comment.value)
        } else {
            echoMust(comment.value)
        }
    }

    fun echo(result: ResultSet) {
        val res = Result(result) // side effect is scanning of hole result set
        if (echoResult) {
            echoMust(ResultConvert.makeResultConvert(outMode, res).convert())
        }
    }

    fun echo(exception: SQLException) {
        val compat = SqlExceptionCompat(exception)

        echoMust(compat.toString())
    }

    fun echo(statement: XStatement, prefix: String = "") {
        if (!echoStatement) {
            return
        }
        when (statement) {
            is SqlStatement -> {
                if (statement.isBlock) {
                    echoMust("$prefix${statement.sql}/")
                } else {
                    echoMust("$prefix${statement.sql};")
                }
            }
            is ShellStatement -> echoMust("$prefix$KEY_SHELL ${statement.cmd};")
            is SetStatement -> echoMust("$prefix$KEY_SET ${statement.attrs.joinToString(" ")};")
            is ConnectStatement -> {
                val msg = when {
                    statement.user.isEmpty() -> {
                        "$prefix$KEY_CONNECT;"
                    }
                    statement.host.isEmpty() -> {
                        "$prefix$KEY_CONNECT ${statement.user}/${statement.password};"
                    }
                    statement.port.isEmpty() -> {
                        "$prefix$KEY_CONNECT ${statement.user}/${statement.password}@${statement.host};"
                    }
                    else -> {
                        "$prefix$KEY_CONNECT ${statement.user}/${statement.password}@${statement.host}:${statement.port};"
                    }
                }
                echoMust(msg)
            }
            is DescStatement -> {
                when (statement.type) {
                    DescStatement.DescType.OBJECT -> {
                        if (statement.schema.isEmpty()) {
                            echoMust("$prefix$KEY_DESCRIBE -o ${statement.table};")
                        } else {
                            echoMust("$prefix$KEY_DESCRIBE -o ${statement.schema}.${statement.table};")
                        }
                    }
                    DescStatement.DescType.QUERY -> echoMust("$prefix$KEY_DESCRIBE -q ${statement.query};")
                }
            }
            is FreeBlockStatement -> {
                echoMust("$prefix${statement.name}\n{    ${statement.content}}")
            }
        }
    }

    fun echo(msg: String) {
        if (echoResult) {
            echoMust(msg)
        }
    }

    var echoStatement: Boolean = true
    var echoResult: Boolean = true
    var echoComment: Boolean = true
    var outMode: String = "pretty"
    var charset: String = "utf-8"
}

class StreamSqlOutput(private val output: OutputStream) : SqlOutput() {
    private val outputLock = ReentrantLock()

    override fun echoMust(msg: String, lf: Boolean) {
        outputLock.withLock {
            output.write(msg.toByteArray(Charset.forName(charset)))
            if (lf) {
                output.write('\n'.code)
            }
        }
    }

    override fun newWithSuffix(suffix: String): FileSqlOutput {
        throw RuntimeException("not support for stream SqlOutput")
    }

    override fun close() {
        output.close()
    }

}

class FileSqlOutput(val output: File) : SqlOutput() {
    private val outputLock = ReentrantLock()
    private var outCanClose = false

    private var outputPrinter: OutputStream by object : ReadWriteProperty<Any?, OutputStream> {
        private var value: OutputStream? = null

        override fun getValue(thisRef: Any?, property: KProperty<*>): OutputStream {
            if (value == null) {
                output.parentFile.mkdirs()
                value = BufferedOutputStream(FileOutputStream(output), FileOutputScript.DEFAULT_BUFFER_SIZE)
                outCanClose = true
            }

            return value!!
        }

        override fun setValue(thisRef: Any?, property: KProperty<*>, value: OutputStream) {
            this.value = value
        }
    }

    override fun echoMust(msg: String, lf: Boolean) {
        outputLock.withLock {
            outputPrinter.write(msg.toByteArray(Charset.forName(charset)))
            if (lf) {
                outputPrinter.write('\n'.code)
            }
        }
    }

    override fun newWithSuffix(suffix: String): FileSqlOutput {
        val res = FileSqlOutput(File("${output.canonicalFile}$suffix"))
        res.charset = charset
        res.echoComment = echoComment
        res.echoResult = echoResult
        res.echoStatement = echoStatement
        res.echoComment = echoComment
        res.outMode = outMode

        return res
    }

    override fun close() {
        if (outCanClose) {
            outputPrinter.close()
        }
    }
}

class SqlScriptBuilder {
    lateinit var nodeName: String
        private set
    lateinit var connectionPool: ConnectionPool
        private set
    var env = mapOf<String, String>()
        private set
    lateinit var output: SqlOutput
        private set
    lateinit var timing: SqlOutput
        private set
    lateinit var log: SqlOutput
        private set
    var user: String? = null
        private set
    var password: String? = null
        private set
    var host: String? = null
        private set
    var port: Int? = null
        private set

    fun nodeName(hostName: String) = apply { this.nodeName = hostName }
    fun connectionPool(connectionPool: ConnectionPool) = apply { this.connectionPool = connectionPool }
    fun env(env: Map<String, String>) = apply { this.env = env }
    fun output(output: SqlOutput) = apply { this.output = output }
    fun timing(timing: SqlOutput) = apply { this.timing = timing }
    fun log(log: SqlOutput) = apply { this.log = log }
    fun user(user: String?) = apply { this.user = user }
    fun password(password: String?) = apply { this.password = password }
    fun host(host: String?) = apply { this.host = host }
    fun port(port: Int?) = apply { this.port = port }

    fun build(type: BaseSqlScript.SqlScriptType): BaseSqlScript {
        return when (type) {
            BaseSqlScript.SqlScriptType.SQLX -> SqlScript(this)
            BaseSqlScript.SqlScriptType.UNIT_SQLX -> UnitSqlScript(this)
            BaseSqlScript.SqlScriptType.PARALL_SQLX -> RandomSqlScript(this)
        }
    }
}

abstract class BaseSqlScript internal constructor(builder: SqlScriptBuilder) : FileOutputScript() {
    companion object {
        private val setStatementChecker = mapOf(
            Pair(KEY_ECHO, IntRange(2, 3)),
            Pair(KEY_AUTOCOMMIT, IntRange(1, 2)),
            Pair(KEY_CHARSET, IntRange(2, 2))
        )

        private const val descSqlCurrentSchema = """
            select 
                C.column_name as Name,
                case C.nullable
                    when 'N' then 'Not Null'
                    else ''
                end as "Null",
                C.data_type as Type
            from my_tab_columns as C
            where C.table_name = ?
        """

        private const val descSqlWithSchema = """
            select 
                C.column_name as Name,
                case C.nullable
                    when 'N' then 'Not Null'
                    else ''
                end as "Null",
                C.data_type as Type
            from adm_tab_columns as C
            where C.table_name = ? and C.owner = ?
        """

        private val strType2SqlType = mapOf(
            Pair("str", Types.CHAR),
            Pair("int", Types.INTEGER),
            Pair("long", Types.BIGINT),
            Pair("float", Types.FLOAT),
            Pair("double", Types.DOUBLE),
            Pair("number", Types.NUMERIC),
            Pair("date", Types.DATE),
            Pair("datetime", Types.TIMESTAMP),
            Pair("time", Types.TIME),
            Pair("bytes", Types.BLOB)
        )
    }

    enum class SqlScriptType { SQLX, UNIT_SQLX, PARALL_SQLX }

    protected var connected = false
    protected var nodeName = builder.nodeName
    protected var user: String? = builder.user
    protected var password: String? = builder.password
    protected var host: String? = builder.host
    protected var port: Int? = builder.port
    protected val connectionPool: ConnectionPool = builder.connectionPool
    protected val env = builder.env
    protected var output = builder.output
    protected val timing = builder.timing
    protected val log = builder.log

    private val bind = Binding()
    private val scriptEngine = GroovyShell(bind)

    private val sessions = mutableMapOf<String, Sessions>()
    private val timings = mutableMapOf<String, Timing>()
    private val asyncSessions = mutableListOf<Thread>()

    data class Timing(val start: LocalDateTime, val duration: Duration)
    data class Sessions(val block: BlockStatement, val script: BaseSqlScript)

    protected var connection: Connection by object : ReadWriteProperty<Any?, Connection> {
        private var value: Connection? = null

        @Suppress("UNCHECKED_CAST")
        override fun getValue(thisRef: Any?, property: KProperty<*>): Connection {
            if (value == null) {
                value = connectionPool.getConnection(nodeName, user, password, host, port)
                connected = true
            }
            return value ?: throw IllegalStateException("Property ${property.name} should be initialized before get.")
        }

        override fun setValue(thisRef: Any?, property: KProperty<*>, value: Connection) {
            this.value = value
        }
    }

    abstract fun execute(script: String): Boolean

    open fun execute(scriptFile: File): Boolean {
        return execute(scriptFile.readText())
    }

    protected fun execSql(sql: SqlStatement): Boolean {
        output.echo(sql)

        val sqlText = MacroReplacer(sql.sql).replace(env)
        return when (sql) {
            is BatchSqlStatement -> execSqlBatchBindParams(sqlText, sql)
            is BindSqlStatement -> execSqlBindParams(sqlText, sql)
            else -> executeSqlText(sqlText)
        }
    }

    private fun execSqlBatchBindParams(sql: String, sqlStatement: BatchSqlStatement): Boolean {
        try {
            connection.prepareStatement(sql).use { statement ->
                sqlStatement.batch.forEach { bindValue ->
                    bindSqlWithParams(statement, bindValue)
                    statement.addBatch()
                }

                statement.executeBatch()
                output.echo("SQL SUCCESS")
            }
        } catch (e: SQLException) {
            output.echo(e)
            return false
        } catch (e: SqlExecuteError) {
            output.echo("${e.message}")
            return false
        }

        return true
    }

    private fun bindSqlWithParams(statement: PreparedStatement, params: BindValues) {
        var bindIndex = 0
        for (param in params) {
            bindIndex++
            val value = param.value

            if (value == null) {
                val sqlType = strType2SqlType[param.type] ?: throw SqlExecuteError("get unknown type ${param.type}")
                statement.setNull(bindIndex, sqlType)
                continue
            }

            when (param.type) {
                "str" -> statement.setString(bindIndex, value)
                "int" -> statement.setInt(bindIndex, value.toInt())
                "long" -> statement.setLong(bindIndex, value.toLong())
                "float" -> statement.setFloat(bindIndex, value.toFloat())
                "double" -> statement.setDouble(bindIndex, value.toDouble())
                "number" -> statement.setBigDecimal(bindIndex, BigDecimal(value))
                "date" -> statement.setDate(bindIndex, Date.valueOf(value))
                "datetime" -> statement.setTimestamp(bindIndex, Timestamp.valueOf(value))
                "time" -> statement.setTime(bindIndex, Time.valueOf(value))
                "bytes" -> statement.setBytes(bindIndex, Hex.decodeHex(value))
            }
        }
    }

    private fun execSqlBindParams(sql: String, sqlStatement: BindSqlStatement): Boolean {
        try {
            connection.prepareStatement(sql).use { statement ->
                bindSqlWithParams(statement, sqlStatement.bind)
                if (statement.execute()) {
                    statement.resultSet.use {
                        output.echo(statement.resultSet)
                    }
                } else {
                    output.echo("SQL SUCCESS")
                }
            }
        } catch (e: SQLException) {
            output.echo(e)
            return false
        } catch (e: SqlExecuteError) {
            output.echo("${e.message}")
            return false
        }

        return true
    }

    private fun executeSqlText(sql: String): Boolean {
        try {
            connection.createStatement().use { statement ->
                if (statement.execute(sql)) {
                    statement.resultSet.use {
                        output.echo(statement.resultSet)
                    }
                } else {
                    output.echo("SQL SUCCESS")
                }
            }
        } catch (e: SQLException) {
            output.echo(e)
            return false
        }

        return true
    }

    protected fun execConnect(connect: ConnectStatement): Boolean {
        output.echo(connect)
        if (connect.node.isNotEmpty()) {
            nodeName = connect.node
            user = null
            password = null
            host = null
            port = null
        } else {
            if (connect.user.isNotEmpty()) {
                user = MacroReplacer(connect.user).replace(env)
                password = MacroReplacer(connect.password).replace(env)
            }
            if (connect.host.isNotEmpty()) {
                host = MacroReplacer(connect.host).replace(env)
            }
            if (connect.port.isNotEmpty()) {
                try {
                    port = MacroReplacer(connect.port).replace(env).toInt()
                } catch (e: NumberFormatException) {
                    output.echo("parse port of connect command error $e")
                    return false
                }
            }
        }

        closeConnection()
        doConnection()
        output.echo("CONNECT SUCCESS")
        return true
    }

    protected fun execSetStatement(set: SetStatement): Boolean {
        output.echo(set)
        if (set.attrs.isEmpty()) {
            output.echo("set statement require at least on params")
            return false
        }

        val checker = setStatementChecker[set.attrs[0]]
        if (checker == null) {
            output.echo("Not support set command, set ${set.attrs[0]} ...")
            return false
        }

        if (set.attrs.size < checker.first || set.attrs.size > checker.last) {
            output.echo("set statement set ${set.attrs[0]} ... require params count: $checker")
            return false
        }

        val res = when (set.attrs[0]) {
            KEY_AUTOCOMMIT -> {
                execAutoCommitStatement(set.attrs)
            }
            KEY_CHARSET -> {
                output.charset = set.attrs[1]
                true
            }
            KEY_ECHO -> {
                execEchoStatement(set.attrs)
            }
            else -> {
                output.echo("Not support set command, set ${set.attrs[0]} ...")
                false
            }
        }

        output.echo("SET SUCCESS")
        return res
    }

    private fun getBool(value: String): Int {
        return if (value.equals("on", true) || value.equals("true", true)) {
            1
        } else if (value.equals("off", true) || value.equals("false", true)) {
            0
        } else {
            -1
        }
    }

    private fun isBool(value: String): Boolean {
        return value in arrayOf("on", "off", "true", "false")
    }

    private fun execAutoCommitStatement(attrs: List<String>): Boolean {
        when (attrs.size) {
            1 -> {
                connection.autoCommit = !connection.autoCommit
            }
            2 -> {
                connection.autoCommit = when (getBool(attrs[1])) {
                    1 -> {
                        true
                    }
                    0 -> {
                        false
                    }
                    else -> {
                        output.echo("invalid value for set autocommit command")
                        return false
                    }
                }
            }
            else -> {
                output.echo("illegal set autocommit command found")
                return false
            }
        }
        return true
    }

    private fun execEchoStatement(attrs: List<String>): Boolean {
        when (attrs.size) {
            1 -> {
                output.echoResult = !output.echoResult
                output.echoComment = !output.echoComment
                output.echoStatement = !output.echoStatement
            }
            2 -> {
                if (isBool(attrs[1])) {
                    val res = when (getBool(attrs[1])) {
                        1 -> true
                        0 -> false
                        else -> {
                            output.echo("illegal value of set echo command found")
                            return false
                        }
                    }
                    output.echoResult = res
                    output.echoComment = res
                    output.echoStatement = res
                }
            }
            3 -> {
                val res = when (getBool(attrs[2])) {
                    1 -> true
                    0 -> false
                    else -> {
                        output.echo("illegal value of set echo command found")
                        return false
                    }
                }
                when (attrs[1]) {
                    KEY_ECHO_COMMENT -> output.echoComment = res
                    KEY_ECHO_RESULT -> output.echoResult = res
                    KEY_ECHO_STATEMENT -> output.echoStatement = res
                    else -> {
                        output.echo("Not support set echo command, set echo ${attrs[2]} ...")
                        return false
                    }
                }
            }
            else -> {
                output.echo("illegal echo statement found")
                return false
            }
        }

        return true
    }

    protected fun execShell(shell: ShellStatement): Boolean {
        output.echo(shell)
        val res = execShellCommand(shell.cmd)

        if (res.stdout.isEmpty()) {
            output.echo("SHELL COMMAND SUCCESS")
        } else {
            output.echo(res.stdout)
        }

        return res.returncode == 0
    }

    protected fun execCommentStatement(comment: CommentStatement): Boolean {
        output.echo(comment)
        return true
    }

    protected fun execDescStatement(desc: DescStatement): Boolean {
        output.echo(desc)
        try {
            connection.createStatement().use { statement ->
                when (desc.type) {
                    DescStatement.DescType.OBJECT -> {
                        val st = if (desc.schema.isEmpty()) {
                            statement.execute("select * from ${desc.table} limit 1")
                            val st = connection.prepareStatement(descSqlCurrentSchema)
                            st.setString(1, desc.table.uppercase())
                            st
                        } else {
                            statement.execute("select * from ${desc.schema}.${desc.table} limit 1")
                            val st = connection.prepareStatement(descSqlWithSchema)
                            st.setString(1, desc.table.uppercase())
                            st.setString(2, desc.schema.uppercase())
                            st
                        }

                        if (st.execute()) {
                            statement.resultSet.use {
                                output.echo(statement.resultSet)
                            }
                        }
                    }
                    DescStatement.DescType.QUERY -> {
                        // NOT SUPPORT NOW
                    }
                }
            }
        } catch (e: SQLException) {
            output.echo(e)
            return false
        }

        return true
    }

    private fun execBlockStatement(block: BlockStatement): Boolean {
        return when (block.name) {
            KEY_ASYNC -> execAsyncStatement(block)
            KEY_SESSION -> execSessionStatement(block)
            KEY_STEP -> execStepStatement(block)
            KEY_FOR -> execForStatement(block)
            KEY_TIMING -> execTimingStatement(block)
            KEY_CBO -> execCboStatement(block)
            KEY_PARALLEL -> execParallelStatement(block)
            else -> {
                output.echo("Not support block statement found with name ${block.name}")
                false
            }
        }
    }

    private fun execParallelStatement(block: BlockStatement): Boolean {
        val allRes = mutableListOf<Future<Boolean>>()
        var finalResult = true

        var stmtIndex = 1
        for (stmt in block.statements) {
            if (stmt is BlockStatement && stmt.name == KEY_SESSION && stmt.properties.contains("name")) {
                output.echo("named session is not allow in parallel statement")
                return false
            }

            allRes.add(WorkPool.pool.submit<Boolean> {
                val newScript = SqlScriptBuilder()
                    .connectionPool(connectionPool)
                    .env(env)
                    .nodeName(nodeName)
                    .output(output.newWithSuffix(".parallel.${stmtIndex++}"))
                    .timing(timing)
                    .log(log)
                    .build(SqlScriptType.SQLX)
                val res = newScript.execXStatement(stmt)
                newScript.close()
                return@submit res
            })
        }
        for (res in allRes) {
            finalResult = res.get() && finalResult
        }
        return finalResult
    }

    private data class CboBody(
        val res: Boolean,
        val sql: SqlStatement? = null,
        val on: List<XStatement> = emptyList(),
        val off: List<XStatement> = emptyList()
    )

    private fun parseCboBody(block: BlockStatement): CboBody {
        var onStmt = emptyList<XStatement>()
        var offStmt = emptyList<XStatement>()
        var sqlStmt: SqlStatement? = null

        block.statements.forEach { statement ->
            if (statement !is BlockStatement) {
                output.echo("only block statement allow in $KEY_CBO block statement")
                return CboBody(false)
            }

            when (statement.name) {
                KEY_ON -> {
                    onStmt = statement.statements
                }
                KEY_OFF -> {
                    offStmt = statement.statements
                }
                KEY_SQL -> {
                    if (statement.statements.size != 1 || statement.statements[0] !is SqlStatement) {
                        output.echo("only one sql statement allow in $KEY_CBO.$KEY_SQL block statement")
                        return CboBody(false)
                    }
                    sqlStmt = statement.statements[0] as SqlStatement
                }
                else -> {
                    output.echo("not support block statement ${statement.name} in $KEY_CBO statement")
                    return CboBody(false)
                }
            }
        }

        return CboBody(true, sqlStmt, onStmt, offStmt)
    }

    protected fun execCboStatement(block: BlockStatement): Boolean {
        if (block.statements.size != 3) {
            output.echo("invalid $KEY_CBO block statement")
            return false
        }

        val cboBody = parseCboBody(block)
        if (!cboBody.res) {
            return false
        }
        if (cboBody.sql == null) {
            output.echo("no $KEY_SQL block found")
        }

        val count = block.properties.getInt("count", 5)
        if (count <= 0) {
            output.echo("$KEY_CBO block's attribute count must > 0")
            return false
        }
        val name = block.properties.get("name")
        if (name == null) {
            output.echo("$KEY_CBO block require attribute name")
            return false
        }
        val compare = block.properties.getDouble("compare", 0.05)

        var res = execXStatements(cboBody.on)
        val onPerf = execExplainAndSql(cboBody.sql!!, count)
        val onResult = execSql(cboBody.sql.sql)
        res = onResult.first && res && onPerf.first

        res = execXStatements(cboBody.off) && res
        val offPerf = execExplainAndSql(cboBody.sql, count)
        val offResult = execSql(cboBody.sql.sql)
        res = offResult.first && res && offPerf.first

        if (resultCompare(onResult.second, offResult.second)) {
            output.echo("RESULT COMPARE SUCCESS")
        } else {
            output.echo("RESULT COMPARE FAILED")
            res = false
        }

        if (dealPerform(name, onPerf.second, offPerf.second, compare)) {
            output.echo("PERFORM COMPARE SUCCESS")
        } else {
            output.echo("PERFORM COMPARE FAILED")
            res = false
        }

        return res
    }

    private fun resultCompare(left: ResultSet?, right: ResultSet?): Boolean {
        if (left == null && right == null) {
            return true
        } else if (left == null || right == null) {
            return false
        }

        if (left.row != right.row) {
            return false
        }

        return true
    }

    private fun dealPerform(name: String, on: Array<Long>, off: Array<Long>, compare: Double): Boolean {
        val onAvg = getAvgAndPrint(name, "on", on)
        val offAvg = getAvgAndPrint(name, "off", off)

        return when {
            offAvg < 0.1 -> {
                onAvg < 2
            }
            onAvg < offAvg -> {
                true
            }
            else -> {
                (onAvg - offAvg) / offAvg <= compare
            }
        }
    }

    private fun getAvgAndPrint(name: String, stage: String, res: Array<Long>): Double {
        res.forEachIndexed { idx, time ->
            output.echo("$name.$stage[$idx] = $time")
        }

        val average = if (res.size > 3) {
            res.slice(IntRange(1, res.size - 2)).average()
        } else {
            res.average()
        }
        output.echo("$name.$stage.avg = $average")
        return average
    }

    protected fun execSql(sql: String): Pair<Boolean, ResultSet?> {
        try {
            connection.createStatement().use { stmt ->
                stmt.execute(sql)
                return Pair(true, stmt.resultSet)
            }
        } catch (e: SQLException) {
            output.echo(e)
            return Pair(false, null)
        }
    }

    private fun execExplainAndSql(sql: SqlStatement, count: Int): Pair<Boolean, Array<Long>> {
        var res = execSql(SqlStatement("explain ${sql.sql}", false))

        val timings = Array<Long>(count) { 0 }

        (0 until count).forEach { i ->
            try {
                val bench = Benchmark()
                connection.createStatement().use { stmt ->
                    stmt.execute(sql.sql)
                    val resultSet = stmt.resultSet
                    if (resultSet != null) {
                        while (resultSet.next()) { /* do nothing */
                        }
                    }
                }
                timings[i] = bench.finish().toMillis()
            } catch (e: SQLException) {
                output.echo(e)
                res = false
            }
        }

        Arrays.sort(timings)

        return Pair(res, timings)
    }

    protected fun execTimingStatement(block: BlockStatement): Boolean {
        val name = block.properties.get("name")
        if (name == null) {
            output.echo("require timing block properties name")
            return false
        }
        if (timings.containsKey(name)) {
            output.echo("duplicate timing name found $name")
            return false
        }

        val bench = Benchmark()

        var res = true
        block.statements.forEach {
            res = execXStatement(it) && res
        }

        timings[name] = Timing(bench.begin, bench.finish())
        timing.echo("$name = ${timings[name]!!.duration.toMillis()}")
        return res
    }

    private fun execStepsStatement(steps: StepsStatement): Boolean {
        var res = true
        steps.steps.forEach { step ->
            val session = sessions[step.session]
            if (session == null) {
                output.echo("Session block with value ${step.session} is not exists")
                return false
            } else {
                if (step.index < session.block.statements.size) {
                    val statement = session.block.statements[step.index]
                    val stepResult = session.script.execXStatement(statement)

                    res = stepResult && res
                } else {
                    output.echo("Session block with value ${step.session} do not have statement with index ${step.index}")
                    return false
                }
            }
        }

        return res
    }

    private fun execStepStatement(block: BlockStatement): Boolean {
        var res = true
        block.statements.forEach { statement ->
            val itemRes = when (statement) {
                is BlockStatement -> {
                    output.echo("Block statement is not allow in step block")
                    false
                }
                is ShellStatement -> execShell(statement)
                is SqlStatement -> execSql(statement)
                is ConnectStatement -> execConnect(statement)
                is StepsStatement -> {
                    output.echo("steps statement is not allow in step block")
                    false
                }
                is SetStatement -> execSetStatement(statement)
                is DescStatement -> execDescStatement(statement)
                is CommentStatement -> {
                    true
                }
                else -> {
                    output.echo("Not support statement found $statement")
                    false
                }
            }
            res = itemRes && res
        }
        return res
    }

    private fun execAsyncStatement(@Suppress("UNUSED_PARAMETER") block: BlockStatement): Boolean {
        return true
    }

    private fun execSessionStatement(block: BlockStatement): Boolean {
        val builder = SqlScriptBuilder()
        val realNode = block.properties.get("node")

        if (realNode == null) {
            builder.nodeName(nodeName)
                .user(block.properties.get("user") ?: user)
                .password(block.properties.get("password") ?: password)
                .host(block.properties.get("host") ?: host)
                .port(block.properties.getInt("port") ?: port)
        } else {
            builder.nodeName(realNode)
                .port(block.properties.getInt("port"))
                .user(block.properties.get("user"))
                .password(block.properties.get("password"))
                .host(block.properties.get("host"))
        }

        val script = builder
            .connectionPool(connectionPool)
            .env(env)
            .log(log)
            .timing(timing)
            .output(output)
            .build(SqlScriptType.SQLX)

        when (val name = block.properties.get("name")) {
            null -> {
                return script.execXStatements(block.statements)
            }
            in sessions -> {
                output.echo("Duplicate session defined with value: $name")
                return false
            }
            else -> {
                sessions[name] = Sessions(block, script)
            }
        }

        return true
    }

    internal fun execXStatement(statement: XStatement): Boolean {
        return when (statement) {
            is BlockStatement -> execBlockStatement(statement)
            is FreeBlockStatement -> execFreeBlockStatement(statement)
            is StepsStatement -> execStepsStatement(statement)
            else -> execNoBlockStatement(statement)
        }
    }

    protected fun execXStatements(statement: List<XStatement>): Boolean {
        var res = true
        statement.forEach {
            res = execXStatement(it) && res
        }

        return res
    }

    protected fun execFreeBlockStatement(statement: FreeBlockStatement): Boolean {
        return when (statement.name) {
            KEY_COMPARE -> execCompareStatement(statement)
            KEY_EVAL -> execEval(statement)
            KEY_PROXY -> execZSql(statement)
            else -> {
                output.echo("not support free block ${statement.name} found")
                false
            }
        }
    }

    private fun execZSql(statement: FreeBlockStatement): Boolean {
        output.echo(statement)

        return true
    }

    protected fun execEval(statement: FreeBlockStatement): Boolean {
        output.echo(statement)

        timings.forEach { (variable, value) ->
            bind.setVariable(variable, value.duration.toMillis())
        }

        try {
            output.echo(scriptEngine.evaluate(statement.content).toString())
        } catch (e: Exception) {
            output.echo("EVAL ERROR: $e")
            return false
        }

        return true
    }

    protected fun execCompareStatement(statement: FreeBlockStatement): Boolean {
        output.echo(statement)

        val bind = Binding()
        timings.forEach { (variable, value) ->
            bind.setVariable(variable, value.duration.toMillis())
        }
        val scriptEngine = GroovyShell(bind)

        return try {
            val res = scriptEngine.evaluate(statement.content) as Boolean
            if (res) {
                output.echo("COMPARING SUCCESS")
                true
            } else {
                output.echo("COMPARING FAILED")
                false
            }
        } catch (e: Exception) {
            output.echoMust("COMPARING ERROR: $e")
            false
        }
    }

    protected fun execNoBlockStatement(statement: XStatement): Boolean {
        return when (statement) {
            is SqlStatement -> execSql(statement)
            is SetStatement -> execSetStatement(statement)
            is ConnectStatement -> execConnect(statement)
            is ShellStatement -> execShell(statement)
            is CommentStatement -> execCommentStatement(statement)
            is DescStatement -> execDescStatement(statement)
            else -> {
                output.echo("Not support command found")
                false
            }
        }
    }

    protected fun execForStatement(block: BlockStatement): Boolean {
        val count = block.properties.getInt("count", 1)

        val timingType = block.properties.get("timing_type", "sum")
        val timingName = block.properties.get("timing")

        val bench = Benchmark()
        var res = true
        (1..count).forEach { _ ->
            block.statements.forEach {
                res = execXStatement(it) && res
            }
        }
        val duration = bench.finish()

        if (timingName != null) {
            if (timings.containsKey(timingName)) {
                output.echo("duplicate timing $timingName")
                return false
            }

            val useTime = when (timingType) {
                "average" -> duration.toMillis() / count
                "sum" -> duration.toMillis()
                else -> {
                    output.echo("not support timing type $timingType")
                    return false
                }
            }
            timings[timingName] = Timing(bench.begin, Duration.ofMillis(useTime))
            timing.echo("$timingName = ${timings[timingName]!!.duration.toMillis()}")
        }

        return res
    }

    private fun execShellCommand(cmd: String): CommandResult {
        return ShellCommander().ssexec(cmd, env)
    }

    protected fun doConnection() {
        if (!connected) {
            connection = connectionPool.getConnection(nodeName, user, password, host, port)
            connected = true
        }
    }

    protected fun newConnection(
        node: String, user: String? = null, password: String? = null, host: String? = null, port: Int? = null
    ): Connection {
        return connectionPool.getConnection(node, user, password, host, port)
    }

    protected fun closeConnection() {
        if (connected) {
            try {
                connection.close()
            } catch (e: Exception) {
                // do nothing
            }
            connected = false
        }
    }

    protected fun switchOutput(writer: SqlOutput): SqlOutput {
        val res = output
        output = writer
        return res
    }

    open fun close() {
        output.close()
        timing.close()
        closeConnection()
    }
}