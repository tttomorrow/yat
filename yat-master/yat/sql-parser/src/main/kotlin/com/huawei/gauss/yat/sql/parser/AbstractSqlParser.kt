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

package com.huawei.gauss.yat.sql.parser

import com.huawei.gauss.yat.sql.parser.statement.BatchBindValues
import com.huawei.gauss.yat.sql.parser.statement.BatchSqlStatement
import com.huawei.gauss.yat.sql.parser.statement.BindSqlStatement
import com.huawei.gauss.yat.sql.parser.statement.BindValues
import com.huawei.gauss.yat.sql.parser.statement.BlockStatement
import com.huawei.gauss.yat.sql.parser.statement.CommentStatement
import com.huawei.gauss.yat.sql.parser.statement.ConnectStatement
import com.huawei.gauss.yat.sql.parser.statement.DescStatement
import com.huawei.gauss.yat.sql.parser.statement.FreeBlockStatement
import com.huawei.gauss.yat.sql.parser.statement.SetStatement
import com.huawei.gauss.yat.sql.parser.statement.ShellStatement
import com.huawei.gauss.yat.sql.parser.statement.SlashStatement
import com.huawei.gauss.yat.sql.parser.statement.SqlStatement
import com.huawei.gauss.yat.sql.parser.statement.StepsStatement
import com.huawei.gauss.yat.sql.parser.statement.XStatement
import java.io.Reader
import java.util.*

abstract class AbstractSqlParser(reader: Reader) {
    protected data class BlockResult(val isBlock: Boolean, val isEnd: Boolean)

    protected val lexer = SqlLex(reader)

    private var line = 0
    private var col = 0
    private var questionCounter = 0;

    private var statementCache: XStatement? = null

    fun nextStatement(): XStatement {
        return if (statementCache == null) {
            parse() ?: throw NoSqlExists()
        } else {
            val res = statementCache
            statementCache = null
            res!!
        }
    }

    fun hasNext(): Boolean {
        return if (statementCache == null) {
            statementCache = parse()
            statementCache != null
        } else {
            true
        }
    }

    protected fun getNextSymbolToken(skipBlank: Boolean = true, skipFeed: Boolean = true): SqlToken {
        val token = getNextToken(skipBlank, skipFeed)
        when {
            token.isSymbol() -> return token
            else -> throw parseError("expect symbol token, found ${token.originValue()}")
        }
    }

    protected fun getNextWordToken(skipFeed: Boolean = true, skipBlank: Boolean = true): SqlToken {
        val token = getNextToken(skipBlank, skipFeed)
        when {
            token.isWord() -> return token
            else -> throw parseError("expect word token, found ${token.originValue()}")
        }
    }

    protected fun getNextValueToken(skipBlank: Boolean = true, skipFeed: Boolean = true): SqlToken {
        val token = getNextToken(skipBlank, skipFeed)
        when {
            token.isValue() -> return token
            else -> throw parseError("expect value token, found ${token.originValue()}")
        }
    }

    protected fun getNextToken(skipBlank: Boolean = true, skipFeed: Boolean = true): SqlToken {
        skip(skipBlank, skipFeed)
        return nextToken() ?: throw parseError("expect token, EOF found")
    }

    protected fun peekNextToken(skipBlank: Boolean = true, skipFeed: Boolean = true): SqlToken {
        skip(skipBlank, skipFeed)

        return peekToken() ?: throw parseError("expect token, EOF found")
    }

    protected fun skip(skipBlank: Boolean = true, skipFeed: Boolean = true): SqlToken? {
        return if (skipBlank && skipFeed) {
            skipSymbolTokens(blankAndFeed)
        } else if (skipBlank) {
            skipSymbolTokens(blank)
        } else if (skipFeed) {
            skipSymbolTokens(feed)
        } else {
            peekToken()
        }
    }

    protected fun skipSymbolTokens(tokens: Map<SqlToken.Type, String>): SqlToken? {
        var token = peekToken()
        while (token != null && token.type in tokens) {
            nextToken()
            token = peekToken()
        }

        return token
    }

    private val caches = LinkedList<SqlToken?>()

    protected fun nextToken(): SqlToken? {
        val token = if (caches.isEmpty()) {
            lexer.nextToken()
        } else {
            caches.poll()
        }

        if (token != null) {
            line = token.position.line
            col = token.position.col
        }

        return token
    }

    protected fun peekToken(index: Int = 0): SqlToken? {
        if (caches.size <= index) {
            val count = caches.size - index + 1
            (1..count).forEach { _ ->
                caches.add(lexer.nextToken())
            }
        }

        return caches[index]
    }

    // parser methods
    protected abstract fun parse(): XStatement?

    protected fun parseCommon(): XStatement? {
        val token = skip() ?: return null

        return when {
            token.isValue() && token.isWord() -> {
                parseStatement()
            }
            token.isComment() -> {
                nextToken()
                CommentStatement(token.originValue(), token.isMultilineComment())
            }
            else -> {
                parseSqlStatement()
            }
        }
    }

    protected fun parseStatement(): XStatement {
        val token = peekNextToken()
        return when (token.originValue()) {
            KEY_SET -> {
                parseSetStatement()
            }
            KEY_SHELL, KEY_SH -> {
                parseShellStatement()
            }
            KEY_CONN, KEY_CONNECT -> {
                parseConnectStatement()
            }
            KEY_ASYNC, KEY_SESSION, KEY_STEP,
            KEY_FOR, KEY_TIMING, KEY_CBO, KEY_ON,
            KEY_OFF, KEY_SQL, KEY_PARALLEL -> {
                parseBlock()
            }
            KEY_STEPS -> {
                parseStepsStatement()
            }
            KEY_DESC, KEY_DESCRIBE -> {
                parseDescStatement()
            }
            KEY_COMPARE, KEY_EVAL, KEY_PROXY -> {
                parseFreeBlock()
            }
            else -> parseSqlStatement()
        }
    }

    protected fun parseFreeBlock(): FreeBlockStatement {
        val name = getNextWordToken()

        val symbol = getNextSymbolToken()
        if (!symbol.isLeftBrace()) {
            throw parseError("expect {, found ${symbol.value}")
        }

        return FreeBlockStatement(name.value, readFreeBlockContent())
    }

    protected fun readFreeBlockContent(): String {
        var token = getNextToken(skipBlank = false, skipFeed = false)
        var leftBraceCount = 0

        val buffer = mutableListOf<String>()
        while (true) {
            when {
                token.isRightBrace() -> {
                    if (leftBraceCount == 0) {
                        return buffer.joinToString("")
                    } else {
                        append(buffer, token)
                        --leftBraceCount
                    }
                }
                token.isBackSlash() -> {
                    token = getNextToken(skipBlank = false, skipFeed = false)
                    when {
                        token.isBackSlash() -> append(buffer, token)
                        token.isRightBrace() -> append(buffer, token)
                        else -> throw parseError("unknown escape charset found \\${token.value[0]}")
                    }
                }
                token.isLeftBrace() -> {
                    append(buffer, token)
                    ++leftBraceCount
                }
                else -> append(buffer, token)
            }

            token = getNextToken(skipBlank = false, skipFeed = false)
        }
    }

    protected fun parseStepsStatement(): StepsStatement {
        val stepsToken = getNextWordToken()
        if (!stepsToken.equalsIgnoreCase(KEY_STEPS)) {
            throw parseError("parse steps statement, expect steps, found ${stepsToken.originValue()}")
        }

        if (!getNextSymbolToken(skipFeed = false, skipBlank = false).isBlank()) {
            throw parseError("parse steps statement, expect a white space or tab")
        }

        val steps = mutableListOf<StepsStatement.Step>()

        while (true) {
            val token = getNextToken()
            when {
                token.isSemicolon() -> return StepsStatement(steps)
                token.isValue() -> {
                    val stepStr = token.value
                    if (stepStr.length < 3) {
                        throw parseError("parse steps statement, illegal step for execute statement")
                    }
                    val dotIndex = stepStr.lastIndexOf('.')
                    if (dotIndex == 0 || dotIndex == -1 || dotIndex == stepStr.lastIndex) {
                        throw parseError("parse steps statement, illegal step for execute statement")
                    }
                    val session = stepStr.substring(0, dotIndex)
                    val stepIndex = try {
                        stepStr.substring(dotIndex + 1).toInt()
                    } catch (e: NumberFormatException) {
                        throw parseError("parse steps statement, illegal step index")
                    }
                    steps.add(StepsStatement.Step(session, stepIndex))
                }
            }
        }
    }

    protected fun parseShellStatement(): ShellStatement {
        val shell = getNextWordToken()
        if (!shell.equals(KEY_SHELL) && !shell.equalsIgnoreCase(KEY_SH)) {
            throw parseError("parse shell statement, expect $KEY_SHELL/$KEY_SH, found ${shell.originValue()}")
        }

        if (!getNextSymbolToken(skipFeed = false, skipBlank = false).isBlank()) {
            throw parseError("parse shell statement, expect a white space or tab")
        }

        return ShellStatement(parseInlineCommand())
    }

    protected fun parseBlock(): BlockStatement {
        val name = getNextWordToken()

        val symbol = getNextSymbolToken()
        var prop = mapOf<String, String>()
        val statements = if (symbol.isLeftBracket()) {
            prop = parseProperties()
            if (getNextSymbolToken().isLeftBrace()) {
                parseBody()
            } else {
                throw parseError("parse ${name.originValue()} block, expect {")
            }
        } else if (symbol.isLeftBrace()) {
            parseBody()
        } else {
            throw parseError("parse ${name.originValue()} block, expect { or (")
        }

        return BlockStatement(name.value, prop, statements)
    }

    protected fun parseProperties(): Map<String, String> {
        val prop = mutableMapOf<String, String>()

        while (true) {
            val token = getNextToken()
            when {
                token.isWord() -> {
                    val key = token.value
                    if (!getNextSymbolToken().isColon()) {
                        throw parseError("parse properties, expect :")
                    }
                    val value = getNextValueToken().value
                    prop[key] = value

                    val end = getNextSymbolToken()
                    if (end.isRightBracket()) {
                        return prop
                    } else if (!end.isComma()) {
                        throw parseError("parse properties, expect , or )")
                    }
                }
                token.isRightBrace() -> throw parseError("parse properties, expect word token")
            }
        }
    }

    protected fun parseBody(): List<XStatement> {
        val statements = mutableListOf<XStatement>()

        while (true) {
            val token = peekNextToken()
            val parseStatement = when {
                token.isRightBrace() -> {
                    // end of the body
                    nextToken()
                    return statements
                }
                else -> {
                    parseCommon()
                }
            }

            if (parseStatement != null) {
                statements.add(parseStatement)
            }
        }
    }

    protected fun parseConnectStatement(): ConnectStatement {
        val conn = getNextWordToken()
        if (!conn.equalsIgnoreCase(KEY_CONN) && !conn.equalsIgnoreCase(KEY_CONNECT)) {
            throw parseError("parse connect statement, expect $KEY_CONN/$KEY_CONNECT, found ${conn.originValue()}")
        }

        if (peekNextToken().isSemicolon()) {
            nextToken()
            return ConnectStatement()
        }

        val user = getNextValueToken()
        val slash = getNextSymbolToken(skipFeed = false, skipBlank = false)
        if (slash.isSemicolon()) {
            return ConnectStatement(node = user.value)
        } else if (!slash.isSlash()) {
            throw parseError("parse connect statement, expect / or ;, but found ${slash.originValue()}")
        }

        val passAndIP = getNextValueToken(skipFeed = false, skipBlank = false)
        val token = getNextSymbolToken(skipBlank = false, skipFeed = false)
        if (token.isWhiteSpace() || token.isTab() || token.isCR() || token.isLF()) {
            if (getNextSymbolToken().isSemicolon()) {
                return ConnectStatement(user.value, passAndIP.value)
            } else {
                throw parseError("parse connect statement, expect ;")
            }
        } else if (token.isSemicolon()) {
            return ConnectStatement(user.value, passAndIP.value)
        } else if (token.isColon()) {
            val port = getNextValueToken(skipFeed = false, skipBlank = false)
            if (passAndIP.value.length < 3) {
                throw parseError("bad connect statement found")
            }

            val lastAtIndex = passAndIP.value.lastIndexOf('@')
            if (lastAtIndex == -1 || lastAtIndex == passAndIP.value.length - 1 || lastAtIndex == 0) {
                throw parseError("bad connect statement found")
            } else {
                if (getNextSymbolToken().isSemicolon()) {
                    return ConnectStatement(
                            user.value,
                            passAndIP.value.substring(0, lastAtIndex - 1),
                            passAndIP.value.substring(lastAtIndex + 1),
                            port.value)
                } else {
                    throw parseError("parse connect statement, expect ;")
                }

            }
        } else {
            throw parseError("unexpect end of connect statement")
        }
    }

    private fun parseSchemaAndTable(value: String): DescStatement {
        return if (value.contains('.')) {
            val splitRes = value.split('.')
            if (splitRes.size != 2) {
                throw parseError("parse desc -o, expect Schema.Table, but found ${value}")
            }
            DescStatement(DescStatement.DescType.OBJECT, splitRes[1], splitRes[0])
        } else {
            DescStatement(DescStatement.DescType.OBJECT, value, "")
        }
    }

    protected fun parseDescStatement(): DescStatement {
        val descToken = getNextWordToken()
        if (!descToken.equalsIgnoreCase(KEY_DESC) && !descToken.equalsIgnoreCase(KEY_DESCRIBE)) {
            throw parseError("parse desc statement, expect desc or describe, found ${descToken.originValue()}")
        }

        var token = getNextWordToken()
        return when {
            token.equalsIgnoreCase("-o") -> {
                token = getNextSymbolToken()
                if (!getNextSymbolToken().isSemicolon()) {
                    throw parseError("parse desc comment, expect ;, but found ${token.originValue()}")
                }
                parseSchemaAndTable(token.value)
            }
            token.equals("-q") -> {
                if (!getNextWordToken().equalsIgnoreCase("select")) {
                    throw parseError("parse desc command, expect select, but found ${token.originValue()}")
                }
                val express = parseUntil(SqlToken.Type.SEMICOLON)
                DescStatement(DescStatement.DescType.QUERY, "select $express")
            }
            else -> {
                if (!getNextSymbolToken().isSemicolon()) {
                    throw parseError("parse desc comment, expect ;, but found ${token.originValue()}")
                }
                parseSchemaAndTable(token.value)
            }
        }
    }

    protected fun parseSetStatement(): XStatement {
        val set = getNextValueToken()
        if (!set.equalsIgnoreCase(KEY_SET)) {
            throw parseError("parse set statement, expect $KEY_SET, but found ${set.originValue()}")
        }

        val res = mutableListOf<String>()

        var token = getNextToken()
        while (!token.isSemicolon()) {
            res.add(token.value)
            token = getNextToken()
        }

        return SetStatement(res)
    }

    protected fun parseSlashCommand(): SlashStatement {
        val slash = getNextSymbolToken()
        if (!slash.isBackSlash()) {
            throw parseError("parse slash statement, expect \\, found ${slash.originValue()}")
        }

        val commandToken = getNextValueToken(skipFeed = false, skipBlank = false)
        val command = commandToken.value
        if (!getNextSymbolToken(skipFeed = false, skipBlank = false).isBlank()) {
            throw parseError("parse slash statement, expect a white space or tab")
        }

        return SlashStatement(command, parseInlineCommand())
    }

    protected fun parseInlineCommand(): String {
        val buffer = mutableListOf<String>()

        var token = getNextToken(skipBlank = false, skipFeed = false)
        while (true) {
            if (token.isSemicolon()) {
                return buffer.joinToString("")
            } else if (token.isLF() || token.isCR()) {
                throw parseError("parse inline statement, expect ;, found CR or LF")
            } else {
                append(buffer, token)
            }

            token = getNextToken(skipBlank = false, skipFeed = false)
        }
    }

    protected fun parseSqlStatement(): SqlStatement {
        val token = getNextToken()

        val buffer = mutableListOf<String>()
        questionCounter = 0
        append(buffer, token)

        val endMark = when {
            token.equalsIgnoreCase("create") -> {
                val res = trySqlBlock(buffer)
                if (res.isBlock) {
                    SqlToken.Type.SLASH
                } else {
                    if (res.isEnd) {
                        val sqlText = buffer.joinToString("")
                        return if (questionCounter > 0) {
                            parseBindSql(sqlText, false)
                        } else {
                            SqlStatement(sqlText, false)
                        }
                    }
                    SqlToken.Type.SEMICOLON
                }
            }
            token.equalsIgnoreCase("declare") || token.equalsIgnoreCase("begin") -> {
                SqlToken.Type.SLASH
            }
            else -> SqlToken.Type.SEMICOLON
        }

        if (endMark == SqlToken.Type.SEMICOLON) {
            append(buffer, parseUntil(endMark))
        } else {
            append(buffer, parseUntilBlockEnd())
        }

        val sqlText = buffer.joinToString("")
        val isBlock = endMark == SqlToken.Type.SLASH

        return if (questionCounter > 0) {
            parseBindSql(sqlText, isBlock)
        } else {
            SqlStatement(sqlText, isBlock)
        }
    }

    protected fun parseBindSql(sql: String, isBlock: Boolean): SqlStatement {
        val nextToken = peekNextToken()
        if (!nextToken.isWord()) {
            throw parseError("parse sql, bind sql require bind block here")
        }

        return when {
            nextToken.equals(KEY_BATCH) -> BatchSqlStatement(sql, isBlock, parseBatchBindValues(questionCounter))
            nextToken.equals(KEY_BIND) -> BindSqlStatement(sql, isBlock, parseBindValues(questionCounter))
            else -> throw parseError("parse sql, unknown bind block found: ${nextToken.originValue()}")
        }
    }

    protected fun parseBatchBindValues(count: Int): BatchBindValues {
        var token = getNextWordToken()
        if (!token.equals(KEY_BATCH)) {
            throw parseError("parse batch bind value, expect $KEY_BATCH, but found ${token.originValue()}")
        }

        token = getNextSymbolToken()
        if (!token.isLeftBrace()) {
            throw parseError("parse batch bind value, expect {, but found ${token.originValue()}")
        }

        val res = BatchBindValues()
        token = peekNextToken()

        while (!token.isRightBrace()) {
            res.add(parseOneBindValue(count))
            token = peekNextToken()
        }

        nextToken()
        return res
    }

    protected fun parseOneBindValue(count: Int): BindValues {
        val res = BindValues(count)

        (1..count).forEach { _ ->
            val token = getNextWordToken()
            val value = getNextToken()
            val itemValue: String? = if (value.isWord()) {
                if (value.value.equals(KEY_NULL, true)) {
                    null
                } else {
                    value.value
                }
            } else if (value.isSingleQuote()) {
                value.value
            } else {
                throw parseError("parse bind value, expect single quote value or word, but found ${value.value}")
            }
            res.add(BindValues.BindItem(token.value, itemValue))
        }

        return res
    }

    protected fun parseBindValues(count: Int): BindValues {
        var token = getNextWordToken()
        if (!token.equals(KEY_BIND)) {
            throw parseError("parse bind value, expect $KEY_BIND, but found ${token.originValue()}")
        }

        token = getNextSymbolToken()
        if (!token.isLeftBrace()) {
            throw parseError("parse bind value, expect {, but found ${token.originValue()}")
        }

        val res = parseOneBindValue(count)

        token = getNextSymbolToken()
        if (!token.isRightBrace()) {
            throw parseError("parse bind value, expect }, but found ${token.originValue()}")
        }

        return res
    }

    protected fun parseUntilBlockEnd(): String {
        val buffer = mutableListOf<String>()

        var token = getNextToken(skipBlank = false, skipFeed = false)
        while (true) {
            if (token.type == SqlToken.Type.SEMICOLON) {
                append(buffer, token)
                token = getNextToken(skipBlank = false, skipFeed = false)

                while (token.type in blankAndFeed) {
                    append(buffer, token)
                    token = getNextToken(skipBlank = false, skipFeed = false)
                }

                if (token.type == SqlToken.Type.SLASH) {
                    return buffer.joinToString("")
                } else {
                    append(buffer, token)
                }
            } else {
                append(buffer, token)
            }
            token = getNextToken(skipFeed = false, skipBlank = false)
        }
    }

    protected fun parseUntil(endMark: SqlToken.Type): String {
        val buffer = mutableListOf<String>()
        var sqlToken = getNextToken(skipBlank = false, skipFeed = false)
        while (true) {
            if (sqlToken.type == endMark) {
                return buffer.joinToString("")
            } else {
                append(buffer, sqlToken)
            }
            sqlToken = getNextToken(skipBlank = false, skipFeed = false)
        }
    }

    protected fun trySqlBlock(buffer: MutableList<String>): BlockResult {
        val token = appendUntilNotNull(buffer)
        return when {
            token.isSymbol() -> parseEnd(token)
            token.isValue() -> when {
                token.equalsIgnoreCase("procedure") -> BlockResult(isBlock = true, isEnd = false)
                token.equalsIgnoreCase("function") -> BlockResult(isBlock = true, isEnd = false)
                token.equalsIgnoreCase("trigger") -> BlockResult(isBlock = true, isEnd = false)
                token.equalsIgnoreCase("package") -> BlockResult(isBlock = true, isEnd = false)
                token.equalsIgnoreCase("or") -> parseOrReplace(buffer)
                token.equalsIgnoreCase("if") -> parseIfExists(buffer)
                else -> BlockResult(isBlock = false, isEnd = false)
            }
            else -> throw parseError("found unknown token type $token")
        }
    }

    protected fun parseEnd(token: SqlToken): BlockResult {
        return if (token.isSemicolon()) {
            BlockResult(isBlock = false, isEnd = true)
        } else {
            BlockResult(isBlock = false, isEnd = false)
        }
    }

    protected fun parseOrReplace(buffer: MutableList<String>): BlockResult {
        val token = appendUntilNotNull(buffer)
        return when {
            token.isSymbol() -> parseEnd(token)
            token.equalsIgnoreCase("replace") -> trySqlBlock(buffer)
            else -> BlockResult(isBlock = false, isEnd = false)
        }
    }

    protected fun parseIfExists(buffer: MutableList<String>): BlockResult {
        var token = appendUntilNotNull(buffer)

        return when {
            token.isSymbol() -> parseEnd(token)
            token.equalsIgnoreCase("not") -> {
                token = appendUntilNotNull(buffer)
                when {
                    token.isSymbol() -> parseEnd(token)
                    token.equalsIgnoreCase("exists") -> trySqlBlock(buffer)
                    else -> BlockResult(isBlock = false, isEnd = false)
                }
            }
            token.equalsIgnoreCase("exists") -> trySqlBlock(buffer)
            else -> BlockResult(isBlock = false, isEnd = false)
        }
    }

    protected fun appendUntilNotNull(buffer: MutableList<String>): SqlToken {
        var token = getNextToken(skipBlank = false, skipFeed = false)

        while (true) {
            if (token.type in blankAndFeed || token.isComment()) {
                append(buffer, token)
            } else {
                append(buffer, token)
                return token
            }
            token = getNextToken(skipBlank = false, skipFeed = false)
        }
    }

    protected fun parseError(msg: String): SqlParseError {
        return SqlParseError(msg, line, col)
    }

    protected fun append(buffer: MutableList<String>, token: SqlToken) {
        if (token.isQuestion()) {
            questionCounter++;
        }
        buffer.add(token.originValue())
        if (token.isLineComemnt()) {
            buffer.add("\n")
        }
    }

    protected fun append(buffer: MutableList<String>, token: String) {
        buffer.add(token)
    }

    protected companion object {
        val blankAndFeed = mapOf(
                Pair(SqlToken.Type.WHITE_SPACE, " "),
                Pair(SqlToken.Type.TAB, "\t"),
                Pair(SqlToken.Type.CR, "\r"),
                Pair(SqlToken.Type.LF, "\n")
        )

        val blank = mapOf(
                Pair(SqlToken.Type.WHITE_SPACE, " "),
                Pair(SqlToken.Type.TAB, "\t")
        )

        val feed = mapOf(
                Pair(SqlToken.Type.CR, "\r"),
                Pair(SqlToken.Type.LF, "\n")
        )
    }
}