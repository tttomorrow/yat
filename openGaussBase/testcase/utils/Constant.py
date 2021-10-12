"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

openGauss is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:

          http://license.coscl.org.cn/MulanPSL2

THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""
'''
    Constants
'''
import sys


class Constant:
    # 定义为类只读属性
    # 停止数据库成功返回信息
    @property
    def STOP_SUCCESS_MSG(self):
        return 'Successfully stopped cluster.'
    
    # 启动数据库成功返回信息
    @property
    def START_SUCCESS_MSG(self):
        return 'Successfully started.'
    
    # 查询数据库状态为启动时返回信息
    @property
    def START_STATUS_MSG(self):
        return 'Normal'
    
    # 查询数据库状态为停止时返回信息
    @property
    def STOP_STATUS_MSG(self):
        return 'stopped'
    
    # 实例正常运行
    @property
    def INSTANCE_RUNNING(self):
        return 'gs_ctl: server is running'
    
    # 使用gs_ctl停止数据库成功返回信息
    @property
    def GS_CTL_STOP_SUCCESS_MSG(self):
        return 'server stopped'
    
    # 连接数据库成功返回信息
    @property
    def CONN_DB_SUCCESS_MSG(self):
        return 'List of databases'
    
    # gs_guc执行成功返回信息
    @property
    def GSGUC_SUCCESS_MSG(self):
        return 'Failed instances: 0.'
    
    # 重建成功返回信息
    @property
    def REBUILD_SUCCESS_MSG(self):
        return 'server started'
    
    # 重建失败信息
    @property
    def BUILD_FAIL_MSG(self):
        return "can't find primary"
    
    # 重建失败信息
    @property
    def BUILD_FAIL_MSG1(self):
        return 'could not connect to server'
    
    # 重建失败信息
    @property
    def BUILD_FAIL_MSG2(self):
        return 'FATAL:  could not load server certificate file "server.crt": no start line'
    
    # 备机磁盘空间不足重建失败信息
    @property
    def NO_SPACE_BUILD_FAIL_MSG(self):
        return ' No space left on device'
    
    # 备机磁盘空间不足重建失败信息
    @property
    def NO_SPACE_BUILD_FAIL_MSG1(self):
        return 'fetch MOT checkpoint'
    
    # 停止某个节点成功返回信息
    @property
    def STOP_NODE_SUC_MSG(self):
        return 'Successfully stopped node.'
    
    # sql语句执行失败后返回信息
    @property
    def SQL_WRONG_MSG(self):
        wrong_msg_seq = ('No relations', 'ERROR', 'Invalid', 'FATAL')
        return wrong_msg_seq
    
    # linux系统中文件不存在返回信息
    @property
    def NO_FILE_MSG(self):
        return 'No such file or directory'
    
    # checkpoint失败信息
    @property
    def FAILED_CHECKPOINT(self):
        return 'connection to server was lost'
    
    # 备机base目录无权限，主机进行create操作，备机pg_log报错相应日志关键信息
    @property
    def REDO_FAILURE_MSG(self):
        return 'aborting  due to page redo process failure'
    
    # REFRESH成功信息
    @property
    def REFRESH_SUCCESS_MSG(self):
        return 'Successfully generated dynamic configuration file.'
    
    # switch执行中信息
    @property
    def SWITCH_ING_MSG(self):
        return 'server starting switchover'
    
    # switch执行成功信息
    @property
    def SWITCH_SUCCESS_MSG(self):
        return 'switchover completed'
    
    # 主节点正常信息
    @property
    def P_NORMAL(self):
        return 'P Primary Normal'
    
    # 备节点正常信息
    @property
    def S_NORMAL(self):
        return 'S Standby Normal'
    
    # 系统日志里面提示归档失败
    @property
    def FAILED_ARCHIVE_MSG(self):
        return "The failed archive command was"
    
    # 表或文件不存在返回信息
    @property
    def NOT_EXIST(self):
        return 'does not exist'
    
    # 创建表成功返回信息
    @property
    def TABLE_CREATE_SUCCESS(self):
        return 'CREATE TABLE'
    
    # 无效状态返回信息
    @property
    def UNAVAILABLE_STATUS(self):
        return 'Unavailable'
    
    # 权限不足返回信息
    @property
    def PERMISSION_DENIED(self):
        return 'permission denied'
    
    # 无法打开文件返回信息
    @property
    def OPEN_FAIL(self):
        return 'could not open file'
    
    # 删除表成功返回信息
    @property
    def TABLE_DROP_SUCCESS(self):
        return 'DROP TABLE'
    
    # 连接失败返回信息
    @property
    def CONN_FAIL(self):
        return 'failed to connect'
    
    # 数据库参数值超出范围提示信息
    @property
    def OUTSIDE_MSG(self):
        return 'is outside the valid range for parameter'
    
    # 连接数据库失败信息
    @property
    def FAILED_CONNECT_DB(self):
        return 'failed to connect Unknown'
    
    # stopped单节点成功信息
    @property
    def STOP_NODE_SUCCESS_MSG(self):
        return 'Successfully stopped node'
    
    # 备节点正常信息
    @property
    def STANDBY_NORMAL(self):
        return 'Standby Normal'
    
    # 主节点正常信息
    @property
    def PRIMARY_NORMAL(self):
        return 'Primary Normal'
    
    # 重启成功信息
    @property
    def RESTART_SUCCESS_MSG(self):
        return 'server started'
    
    # TPCC 失败信息
    @property
    def TPCC_ERROR(self):
        return 'ERROR'
    
    # TPCC refuse
    @property
    def TPCC_REFUSE_MSG(self):
        return 'refused.'
    
    # TPCC success
    @property
    def TPCC_SUCCESS_MSG(self):
        return 'Session End'
    
    @property
    def PERMISSION_DENY_MSG(self):
        return 'Permission denied'
    
    @property
    def SWITCHOVER_SUCCESS_MSG(self):
        return 'switchover completed'
    
    @property
    def REFRESHCONF_SUCCESS_MSG(self):
        return 'Successfully generated dynamic configuration file'
    
    @property
    def CREATE_TABLE_SUCCESS(self):
        return 'CREATE TABLE'
    
    @property
    def DROP_TABLE_SUCCESS(self):
        return 'DROP TABLE'
    
    @property
    def FAILOVER_SUCCESS_MSG(self):
        return 'failover completed'
    
    @property
    def TPCC_CREATE_DATA_SUCCESS_MSG(self):
        return 'indexes built and extra\'s created'
    
    @property
    def DISK_FULL_MSG(self):
        return 'No space left on device'
    
    @property
    def RESTORE_SUCCESS_MSG(self):
        return 'restore operation successful'
    
    @property
    def CFE_DISK_FULL_SUCCESS_MSG(self):
        return 'successful execution [rfile full'
    
    @property
    def CFE_DISK_CLEAN_SUCCESS_MSG(self):
        return 'successful execution [rfile restore'
    
    @property
    def STANDBY_DOWN(self):
        return 'S Down'
    
    @property
    def BUILD_SUCCESS_MSG(self):
        return 'server started'
    
    @property
    def CLUSTER_NORMAL_MSG(self):
        return 'cluster_state   : Normal'
    
    @property
    def BUILD_FAIL_MSG_OPEN(self):
        return 'cannot be opened'
    
    @property
    def CLUSTER_DEGRADED_MSG(self):
        return 'cluster_state   : Degraded'
    
    @property
    def UNRECOGNIZED_SHUTDOWN_MSG(self):
        return 'unrecognized shutdown mode'
    
    @property
    def FAILED_START_MSG(self):
        return 'Failed to start instance'
    
    @property
    def LOGIN_SUCCESS_MSG(self):
        return 'login'
    
    @property
    def LOGOUT_SUCCESS_MSG(self):
        return 'logout'
    
    @property
    def SSL_CONNECTION_CLOSED_MSG(self):
        return 'SSL connection has been closed unexpectedly, remote datanode (null), error: Success'
    
    @property
    def CONNECT_SEVER_SUCCESS_MSG(self):
        return 'connect to sever success, build started.'
    
    @property
    def STOP_NOT_PERMIT_MSG(self):
        return 'Operation not permitted'
    
    @property
    def FUZZY_SEARCH_LIMIT_MSG(self):
    
    @property
    def CREATE_INDEX_SUCCESS_MSG(self):
        return 'CREATE INDEX'
    
    @property
    def DROP_INDEX_SUCCESS_MSG(self):
        return 'DROP INDEX'
    
    @property
    def ALTER_INDEX_SUCCESS_MSG(self):
        return 'ALTER INDEX'
    
    @property
    def REINDEX_SUCCESS_MSG(self):
        return 'REINDEX'
    
    @property
    def REINDEX_FAIL_MSG(self):
        return 'ERROR:  REINDEX DATABASE cannot run inside a transaction block'
    
    @property
    def BACKUP_SUCCESS_MSG(self):
        return 'Successfully backed up cluster files'
    
    @property
    def BACKUP_RESTORE_SUCCESS_MSG(self):
        return 'Successfully restored cluster files'
    
    @property
    def DUMPALL_SUCCESS_MSG(self):
        return 'dumpall operation successful'
    
    @property
    def INSERT_SUCCESS_MSG(self):
        return 'INSERT'
    
    @property
    def DELETE_SUCCESS_MSG(self):
        return 'DELETE'
    
    @property
    def CREATE_ROLE_SUCCESS_MSG(self):
        return 'CREATE ROLE'
    
    @property
    def GRANT_SUCCESS_MSG(self):
        return 'GRANT'
    
    @property
    def REVOKE_SUCCESS_MSG(self):
        return 'REVOKE'
    
    @property
    def CREATE_VIEW_SUCCESS_MSG(self):
        return 'CREATE VIEW'
    
    @property
    def ALTER_VIEW_SUCCESS_MSG(self):
        return 'ALTER VIEW'
    
    @property
    def CREATE_VIEW_FAIL_MSG(self):
        return 'cannot copy to view'
    
    @property
    def LOCK_TABLE_MSG(self):
        return 'LOCK TABLE'
    
    @property
    def ALTER_TABLE_MSG(self):
        return 'ALTER TABLE'
    
    @property
    def COMMIT_SUCCESS_MSG(self):
        return 'COMMIT'
    
    @property
    def START_TRANSACTION_SUCCESS_MSG(self):
        return 'START TRANSACTION'
    
    @property
    def UPDATE_SUCCESS_MSG(self):
        return 'UPDATE'
    
    @property
    def TRUNCATE_SUCCESS_MSG(self):
        return 'TRUNCATE'
    
    @property
    def COPY_PROHIBITED_MSG(self):
        return 'COPY to or from a file is prohibited'
    
    @property
    def COPY_SYNTAX_ERROR_MSG(self):
        return 'syntax error at or near'
    
    @property
    def COPY_INDEX_FAIL_MSG(self):
        return 'is an index'
    
    @property
    def COPY_DIR_ERROR_MSG(self):
        return 'file must under dir'
    
    @property
    def COPY_COLUMN_ERROR_MSG(self):
        return 'extra data after last expected column'
    
    @property
    def COPY_ENCODING_ERROR_MSG(self):
        return 'invalid byte sequence for encoding "SQL_ASCII"'
    
    @property
    def COPY_REQUIRES_ERROR_MSG(self):
        return 'compatible_illegal_chars requires'
    
    @property
    def COPY_FROM_VIEW_FAIL_MSG(self):
        return 'cannot copy from view'
    
    @property
    def INVALID_INPUT_SYNTAX_MSG(self):
        return 'invalid input syntax'
    
    @property
    def VACUUM_TRANSACTION_FAIL_MSG(self):
        return 'VACUUM cannot run inside a transaction block'
    
    @property
    def GSQL_RESTORE_SUCCESS_MSG(self):
        return 'restore operation successful'
    
    # MOT功能不支持数据类型提示信息
    
    @property
    def NOT_SUPPORTED_TYPE(self):
        return 'not supported'
    
    @property
    def OWNER_OF_RELATION_MSG(self):
        return 'must be owner of relation'
    
    # 创建目录对象成功
    @property
    def CREATE_DIRECTORY_SUCCESS_MSG(self):
        return 'CREATE DIRECTORY'
    
    # 删除目录对象成功
    @property
    def DROP_DIRECTORY_SUCCESS_MSG(self):
        return 'DROP DIRECTORY'
    
    # 修改目录对象成功
    @property
    def ALTER_DIRECTORY_SUCCESS_MSG(self):
        return 'ALTER DIRECTORY'
    
    # 语法错误
    @property
    def SYNTAX_ERROR_MSG(self):
        return 'ERROR:  syntax error at or near'
    
    @property
    def UNRECOGNIZED_PRIVILEGE_MSG(self):
        return 'unrecognized privilege type'
    
    @property
    def PRIVILEGE_SYNTAX_ERROR_MSG(self):
        return 'syntax error at or near'
    
    @property
    def ALTER_ROLE_SUCCESS_MSG(self):
        return 'ALTER ROLE'
    
    @property
    def DROP_ROLE_SUCCESS_MSG(self):
        return 'DROP ROLE'
    
    @property
    def CREATE_SCHEMA_SUCCESS_MSG(self):
        return 'CREATE SCHEMA'
    
    @property
    def ALTER_SCHEMA_SUCCESS_MSG(self):
        return 'ALTER SCHEMA'
    
    @property
    def DROP_SCHEMA_SUCCESS_MSG(self):
        return 'DROP SCHEMA'
    
    @property
    def NOT_YET_SUPPORTED_TYPE(self):
        return 'is not yet supported'
    
    @property
    def ACCOUNT_LOCKED_TYPE(self):
        return 'The account has been locked'
    
    @property
    def ACCOUNT_UNLOCKED_TYPE(self):
        return 'The account has been unlocked'
    
    @property
    def INVALID_USERNAME_OR_PASSWD_TYPE(self):
        return 'Invalid username/password,login denied'
    
    @property
    def OUTSIDE_VALID_RANGE_MSG(self):
        return 'outside the valid range for parameter'
    
    @property
    def PASSWORD_CONTAIN_AT_LEAST_MSG(self):
        return 'Password must contain at least'
    
    @property
    def PASSWORD_CANNOT_CONTAIN_MORE_THAN_MSG(self):
        return 'Password can\'t contain more than'
    
    @property
    def CREATE_FOREIGN_SUCCESS_MSG(self):
        return 'CREATE FOREIGN TABLE'
    
    @property
    def DROP_FOREIGN_SUCCESS_MSG(self):
        return 'DROP FOREIGN TABLE'
    
    @property
    def CONFLICT_MSG(self):
        return 'CONFLICT'
    
    @property
    def UNSUPPORTED_ALTER(self):
        return 'does not support alter table'
    
    @property
    def INCLUDING_DEFAULTS(self):
        return 'INCLUDING DEFAULTS'
    
    @property
    def NOT_AS_SELECT(self):
        return 'syntax error at or near "as"'
    
    @property
    def NOT_TABLESPACE(self):
        return 'syntax error at or near "TABLESPACE"'
    
    @property
    def UNLOGGED_MSG(self):
        return 'syntax error at or near "UNLOGGED"'
    
    @property
    def DEFERRABLE_MSG(self):
        return 'is not a table or view'
    
    @property
    def PASSWORD_SHOULD_NOT_EQUAL_MSG(self):
        return 'should not equal to the'
    
    # 创建自定义函数成功
    @property
    def CREATE_FUNCTION_SUCCESS_MSG(self):
        return 'CREATE FUNCTION'
    
    # 创建数据类型成功
    @property
    def CREATE_TYPE_SUCCESS_MSG(self):
        return 'CREATE TYPE'
    
    # 删除数据类型成功
    @property
    def DROP_TYPE_SUCCESS_MSG(self):
        return 'DROP TYPE'
    
    # 修改数据类型成功
    @property
    def ALTER_TYPE_SUCCESS_MSG(self):
        return 'ALTER TYPE'
    
    # 创建视图成功
    @property
    def CREATE_VIEW_SUCCESS_MSG(self):
        return 'CREATE VIEW'
    
    # 删除视图成功
    @property
    def DROP_VIEW_SUCCESS_MSG(self):
        return 'DROP VIEW'
    
    @property
    def TABLESPCE_CREATE_SUCCESS(self):
        return 'CREATE TABLESPACE'
    
    @property
    def TABLESPCE_DROP_SUCCESS(self):
        return 'DROP TABLESPACE'
    
    @property
    def TABLESPCE_ALTER_SUCCESS(self):
        return 'ALTER TABLESPACE'
    
    @property
    def CREATE_INDEX_FAILED(self):
        return 'Total columns size is greater than maximum index size 256'
    
    @property
    def CREATE_INDEX_SUCCESS(self):
        return 'CREATE INDEX'
    
    # 不支持INDEX on NUMERIC or DECIMAL
    @property
    def NOT_SUPPORTED_INDEX(self):
        return 'not supported'
    
    @property
    def CREATE_SEQUENCE_SUCCESS_MSG(self):
        return 'CREATE SEQUENCE'
    
    @property
    def DROP_SEQUENCE_SUCCESS_MSG(self):
        return 'DROP SEQUENCE'
    
    # 删除词典成功
    @property
    def DROP_DICTIONARY_SUCCESS_MSG(self):
        return 'DROP TEXT SEARCH DICTIONARY'
    
    # 创建词典成功
    @property
    def CREATE_DICTIONARY_SUCCESS_MSG(self):
        return 'CREATE TEXT SEARCH DICTIONARY'
    
    # 修改词典成功
    @property
    def ALTER_DICTIONARY_SUCCESS_MSG(self):
        return 'ALTER TEXT SEARCH DICTIONARY'
    
    # 删除文本搜索配置
    @property
    def DROP_TEXT_SEARCH_CONFIGURATION(self):
        return 'DROP TEXT SEARCH CONFIGURATION'
    
    # 创建文本搜索配置
    @property
    def CREATE_TEXT_SEARCH_CONFIGURATION(self):
        return 'CREATE TEXT SEARCH CONFIGURATION'
    
    # 修改文本搜索配置
    @property
    def ALTER_TEXT_SEARCH_CONFIGURATION(self):
        return 'ALTER TEXT SEARCH CONFIGURATION'
    
    @property
    def CREATE_PROCEDURE_SUCCESS_MSG(self):
        return 'CREATE PROCEDURE'
    
    @property
    def DROP_PROCEDURE_SUCCESS_MSG(self):
        return 'DROP PROCEDURE'
    
    @property
    def DROP_FUNCTION_SUCCESS_MSG(self):
        return 'DROP FUNCTION'
    
    @property
    def REPEATABLE_READ_MSG(self):
        return 'repeatable read'
    
    @property
    def READ_COMMITED_MSG(self):
        return 'read committed'
    
    @property
    def READ_ONLY_ERROR_MSG(self):
        return 'cannot execute INSERT in a read-only transaction'
    
    @property
    def DROP_SCHEMA_SUCCESS_MSG(self):
        return 'DROP SCHEMA'
    
    @property
    def SET_TRANSACTION_ERROR_MSG(self):
        return 'SET TRANSACTION ISOLATION LEVEL must be called before any query'
    
    @property
    def NOT_RANGE(self):
        return 'syntax error at or near "RANGE"'
    
    @property
    def CREATE_INDEX_OUTRANGE(self):
        return 'Can not create index, max number of indexes 10 reached'
    
    @property
    def CREATE_ANONYMOUS_BLOCK_SUCCESS_MSG(self):
        return 'ANONYMOUS BLOCK EXECUTE'
    
    @property
    def SET_SUCCESS_MSG(self):
        return 'SET'
    
    @property
    def RESET_SUCCESS_MSG(self):
        return 'RESET'
    
    @property
    def ROLLBACK_MSG(self):
        return 'ROLLBACK'
    
    @property
    def DECLEAR_CURSOR_SUCCESS_MSG(self):
        return 'DECLARE CURSOR'
    
    @property
    def CLOSE_CURSOR_SUCCESS_MSG(self):
        return 'CLOSE CURSOR'
    
    # 创建序列成功
    @property
    def CREATE_SEQUENCE_SUCCESS_MSG(self):
        return 'CREATE SEQUENCE'
    
    # 删除序列成功
    @property
    def DROP_SEQUENCE_SUCCESS_MSG(self):
        return 'DROP SEQUENCE'
    
    # 创建行访问控制策略
    @property
    def CREATE_ROW_LEVEL_SECURITY_POLICY_SUCCESS_MSG(self):
        return 'CREATE ROW LEVEL SECURITY POLICY'
    
    # 修改行访问控制策略
    @property
    def ALTER_ROW_LEVEL_SECURITY_POLICY_SUCCESS_MSG(self):
        return 'ALTER ROW LEVEL SECURITY POLICY'
    
    # 删除行访问控制策略
    @property
    def DROP_ROW_LEVEL_SECURITY_POLICY_SUCCESS_MSG(self):
        return 'DROP ROW LEVEL SECURITY POLICY'
    
    # 查询索引生效
    @property
    def INDEX_BITMAP_SUCCESS_MSG(self):
        return 'Bitmap'
    
    # 删除数据库成功返回信息
    @property
    def DROP_DATABASE_SUCCESS(self):
        return 'DROP DATABASE'
    
    # 创建数据库成功返回信息
    @property
    def CREATE_DATABASE_SUCCESS(self):
        return 'CREATE DATABASE'
    
    # 创建函数
    @property
    def CREATE_FUNCTION_SUCCESS_MSG(self):
        return 'CREATE FUNCTION'
    
    # 修改函数
    @property
    def ALTER_FUNCTION_SUCCESS_MSG(self):
        return 'ALTER FUNCTION'
    
    # 删除函数
    @property
    def DROP_FUNCTION_SUCCESS_MSG(self):
        return 'DROP FUNCTION'
    
    # analyze成功
    @property
    def ANALYZE_SUCCESS_MSG(self):
        return 'ANALYZE'
    
    # vacuum
    @property
    def VACUUM_SUCCESS_MSG(self):
        return 'VACUUM'
    
    @property
    def VACUUM_FAIL_MSG(self):
        return "ERROR:  deltamerge: This relation doesn't support vacuum deltamerge operation"
    
    @property
    def ALTER_DATABASE_SUCCESS_MSG(self):
        return 'ALTER DATABASE'
    
    @property
    def ANALYZE_CASCADE_FAIL_MSG(self):
        return 'ERROR:  The index table does not support verify on cascade mode'
    
    @property
    def ANALYZE_FAIL_MSG(self):
        return 'ERROR:  ANALYZE cannot run inside a transaction block'
    
    @property
    def ANALYZE_DECLARE_FAIL_MSG(self):
        return 'ERROR:  ANALYZE cannot be executed from a function or multi-command string'
    
    @property
    def ALTER_SYSTEM_SUCCESS_MSG(self):
        return 'ALTER SYSTEM'
    
    @property
    def EXPLAIN_SUCCESS_MSG(self):
        return 'QUERY PLAN'
    
    @property
    def EXPLAIN_FAIL_MSG(self):
        return 'ERROR:  EXPLAIN CREATE TABLE AS SELECT requires ANALYZE'
    
    @property
    def PREPARE_SUCCESS_MSG(self):
        return 'PREPARE'
    
    @property
    def CHECKPOINT_SUCCESS_MSG(self):
        return 'CHECKPOINT'
    
    @property
    def AGGREGATE_IN_VALUES_MSG(self):
        return 'cannot use aggregate function in VALUES'
    
    @property
    def PREPARED_TRANSACTION_MSG(self):
        return 'PREPARE TRANSACTION'
    
    @property
    def PREPARED_ROLLBACK_MSG(self):
        return 'ROLLBACK PREPARED'
    
    @property
    def PREPARED_COMMIT_MSG(self):
        return 'COMMIT PREPARED'
    
    # 修改默认权限成功返回信息
    @property
    def ALTER_DEFAULT_PRIVILEGES(self):
        return 'ALTER DEFAULT PRIVILEGES'
    
    # 删除一个数据库角色所拥有的数据库对象，返回成功
    @property
    def DROP_OWNED_SUCCESS(self):
        return 'DROP OWNED'
    
    @property
    def CURSOR_ERROR_MSG(self):
        return 'subprogram body is not ended correctly at end of input'
    
    @property
    def NOT_SUPPORT_INLINE_BLOCK(self):
        return 'not support inline code execution'
    
    # 检查失败配置1
    @property
    def GS_CHECK_ERROR_MSG1(self):
        return 'ERROR: The command must be running with cluster user'
    
    # 单项检查配置（模式）
    @property
    def GS_CHECK_SUCCESS_MSG1(self):
        success_msg_seq1 = ('[RST] OK', '[RST] NG', '[RST] NONE')
        return success_msg_seq1
    
    # 单项检查配置
    @property
    def GS_CHECK_SUCCESS_MSG2(self):
        success_msg_seq2 = (
        'Success', 'Failed', 'All check items run completed')
        return success_msg_seq2
    
    # 收集失败信息
    @property
    def GS_TOOLS_ERROR_MSG1(self):
        return 'Incorrect parameter'
    
    # 收集信息成功
    @property
    def GS_COLLECTOR_SUCCESS_MSG(self):
        return 'Successfully collected files'
    
    # 检查操作系统信息
    @property
    def GS_CHECKOS_SUCCESS_MSG1(self):
        success_msg_seq1 = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8',
                            'A9', 'A10', 'A11', 'A12', 'A13', 'A14']
        return success_msg_seq1
    
    # 检查系统参数
    @property
    def GS_CHECKOS_SUCCESS_MSG2(self):
        success_msg_seq2 = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8']
        return success_msg_seq2
    
    # 数据库启动成功
    @property
    def GS_OM_START_SUCCESS_MSG(self):
        return 'Successfully started'
    
    # 数据库关闭成功
    @property
    def GS_OM_STOP_SUCCESS_MSG(self):
        return 'Successfully stopped cluster'
    
    # 数据库状态正常
    @property
    def GS_OM_STATUS_MSG1(self):
        return 'Normal'
    
    # 数据库状态不可用
    @property
    def GS_OM_STATUS_MSG2(self):
        return 'Unavailable'
    
    # 数据导出成功
    @property
    def GS_DUMP_SUCCESS_MSG(self):
        return 'successfully'
    
    # 导出成功
    @property
    def gs_dumpall_success_msg(self):
        return 'dumpall operation successful'
    
    # 返回开启状态信息
    @property
    def OPEN_STATUS_MSG(self):
        open_status_msgv = ('on', 'true', '1', 'yes')
        return open_status_msgv
    
    # 返回关闭状态信息
    @property
    def CLOSE_STATUS_MSG(self):
        close_status_msgv = ('off', 'false', '0', 'no')
        return close_status_msgv
    
    @property
    def BOOLEAN_VALUES(self):
        boolean_msg = ('on', 'off')
        return boolean_msg
    
    @property
    def INCORRECT_VALUES(self):
        incorrect_msg = ('The value', 'for parameter', 'is incorrect')
        return incorrect_msg
    
    # ngram解析器查询
    @property
    def NGRAM_VALUES_ZH(self):
        results_msg = ('{中文}', '{文检}', '{检索}')
        return results_msg
    
    @property
    def NGRAM_VALUES_EN(self):
        results_msg = ('{he}', '{el}', '{ll}', '{lo}')
        return results_msg
    
    @property
    def NGRAM_VALUES_ALNUM(self):
        results_msg = ('{%a}', '{a%}')
        return results_msg
    
    # 触发器创建成功返回信息
    @property
    def TRIGGER_CREATE_SUCCESS_MSG(self):
        return 'CREATE TRIGGER'
    
    # 触发器删除成功返回信息
    @property
    def TRIGGER_DROP_SUCCESS_MSG(self):
        return 'DROP TRIGGER'
    
    # 参数默认值
    @property
    def SYNCHRONOUS_COMMIT_DEFAULT(self):
        results_msg = ('on', 'off')
        return results_msg
    
    # 修改系统表结构失败
    @property
    def ALTER_SYSTEM_CATALOG_FAIL(self):
        return 'ERROR:  permission denied: "pg_database" is a system catalog'
    
    # 创建数据源
    @property
    def CREATE_DATA_SOURCE_SUCCESS_MSG(self):
        return 'CREATE DATA SOURCE'
    
    # 修改数据源
    @property
    def ALTER_DATA_SOURCE_SUCCESS_MSG(self):
        return 'ALTER DATA SOURCE'
    
    # 删除数据源
    @property
    def DROP_DATA_SOURCE_SUCCESS_MSG(self):
        return 'DROP DATA SOURCE'
    
    # 使用匿名块插入数据
    @property
    def ANONYMOUS_BLOCK_EXECUTE_SUCCESS_MSG(self):
        return 'ANONYMOUS BLOCK EXECUTE'
    
    # 创建同义词
    @property
    def CREATE_SYNONYM_SUCCESS_MSG(self):
        return 'CREATE SYNONYM'
    
    @property
    def invalid_character(self):
        return 'contains invalid character'
    
    @property
    def opengauss(self):
        return 'openGauss'
    
    @property
    def gs_ctl_start_filed(self):
        return 'postgresql.conf cannot be opened'
    
    @property
    def could_not_start_sever(self):
        return 'could not start server'
    
    @property
    def argument_error(self):
        return 'invalid argument'
    
    @property
    def read_file_error(self):
        return 'could not read file'
    
    # gs_ssh执行成功
    @property
    def gs_ssh_success_msg(self):
        return 'Successfully execute command on all nodes.'
    
    @property
    def gs_ctl_reload_success(self):
        return 'server signaled'
    
    @property
    def gs_ctl_status_running(self):
        return 'server is running'
    
    @property
    def gs_ctl_status_norunning(self):
        return 'no server running'
    
    @property
    def upgrading_the_standby(self):
        return 'Standby Normal | 2'
    
    @property
    def upgrading_the_standby_fail(self):
        return 'Primary Normal | 2'
    
    @property
    def trace_start_success(self):
        return '[GAUSS-TRACE] start Success'
    
    @property
    def trace_stop_success(self):
        return '[GAUSS-TRACE] stop Success'
    
    # gs_basebackup执行成功提示信息
    @property
    def gs_basebackup_success_msg(self):
        return 'gs_basebackup: base backup successfully'
    
    @property
    def open_input_file_fail(self):
        return 'Failed to open input file'
    
    @property
    def open_output_file_fail(self):
        return 'Failed to open trace output file'
    
    @property
    def gs_backup_success(self):
        return 'Successfully backed up cluster files'
    
    @property
    def gs_backup_restore_success(self):
        return 'Successfully restored cluster files'
    
    @property
    def root_exec_fail(self):
        return 'Cannot run this script as a user with the root permission'
    
    @property
    def hostname_error(self):
        return 'Failed to obtain the node configuration'
    
    @property
    def init_success(self):
        return 'successfully inited'
    
    @property
    def del_success(self):
        return 'successfully deleted'
    
    @property
    def alter_system_success_msg(self):
        return 'ALTER SYSTEM SET'
    
    @property
    def refresh_success_msg(self):
        return 'Successfully generated dynamic configuration file.'
    
    @property
    def unique_index_error_info(self):
        return 'duplicate key value violates unique constraint'
    
    @property
    def jdbcgsbackup_success(self):
        return 'Connect complete'
    
    @property
    def jdbcgsbackup_failed(self):
        incorrect_msg = ('error', 'failed', 'FATAL')
        return incorrect_msg
    
    @property
    def resource_label_create_success_msg(self):
        return 'CREATE RESOURCE LABEL'
    
    @property
    def resource_label_alter_success_msg(self):
        return 'ALTER RESOURCE LABEL'
    
    @property
    def masking_policy_create_success_msg(self):
        return 'CREATE MASKING POLICY'
