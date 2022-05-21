"""
Copyright (c) 2022 Huawei Technologies Co.,Ltd.

openGauss is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:

          http://license.coscl.org.cn/MulanPSL2

THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""
"""
Case Type   : security_sm4
Case Name   : 表中插入数据时对数据使用sm4加密方式加密，数据插入后对加密数据解密
Description :
    1.创建表table001；
    2.表中插入数据，对address字段加密
    3.查看表中数据，返回信息是否被加密
    4.加密查询出来的结果，作为查询条件查询表数据
    5.将解密查询出来的结果，作为查询条件查询表数据
    6.查看审计日志，检查步骤2-5中语句的信息是否记录正确
    7.查看pg_log日志，检查步骤2-5中语句的信息是否记录正确
Expect      :
    1.创表成功
    2.数据插入完成
    3.返回的信息中，lucy的address信息被加密，显示密文"/lKTzCthzVP+IbmpA+wRzvGQRsw=="
    4.查询出来的address信息未密文“BOI6/lKTzCthzVP+IbmpA+wRzvPMbGQRsw==”
    5.查询出来name字段的信息未为ucy，address字段的信息为“shanxi.xian,yantaqu0569-5“
    6.审计日志中，步骤2和5的操作语句中的加密信息在审计日志中被掩码处理
    7.pg_log日志中，步骤2和5的操作语句中的加密信息在日志中被掩码处理
History     :
"""
import os
import unittest
from time import sleep
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()


class Security(unittest.TestCase):
    def setUp(self):
        logger.info('---Opengauss_Function_Security_sm4_Case0001 start---')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.logfile_name = os.path.join(macro.PG_LOG_PATH, 'dn_6001')

    def test_sm4(self):
        logger.info('--------查看预置参数默认值--------')
        show_param1 = 'show audit_dml_state_select;'
        show_msg1 = self.sh_primy.execut_db_sql(show_param1)
        logger.info(show_msg1)
        global return_msg1, return_msg2, return_msg3
        return_msg1 = show_msg1.splitlines()[2].strip()
        logger.info(return_msg1)
        show_param2 = 'show audit_dml_state;'
        show_msg2 = self.sh_primy.execut_db_sql(show_param2)
        logger.info(show_msg2)
        return_msg2 = show_msg2.splitlines()[2].strip()
        logger.info(return_msg2)
        show_param3 = 'show log_statement;'
        show_msg3 = self.sh_primy.execut_db_sql(show_param3)
        logger.info(show_msg3)
        return_msg3 = show_msg3.splitlines()[2].strip()
        logger.info(return_msg3)
        logger.info('--------修改预置参数--------')
        pre_cmd1 = f'source {self.DB_ENV_PATH};' \
                   f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
                   f'"audit_dml_state_select=1";' \
                   f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
                   f'"audit_dml_state=1";' \
                   f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
                   f'"log_statement=all";'
        pre_msg1 = self.userNode.sh(pre_cmd1).result()
        logger.info(pre_msg1)
        logger.info('------1-2.创建表table001；表中插入数据，对address字段加密----')
        start_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        start_time = start_time_msg.splitlines()[2].strip()
        sleep(5)
        sql_cmd1 = 'create table table001(name char(6),address text);' \
                   'insert into table001 values(\'lucy\',' \
                   'gs_encrypt(\'shanxi.xian,yantaqu0569-5\',' \
                   '\'QAZ2wssx@123\',\'sm4\')),(\'张三\',\'shanxi.xian,' \
                   'yantaqu0569-5\'),(\'李四\',\'shanxi.大同,yantaqu0569-5\');'
        sql_msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(sql_msg1)
        self.assertTrue(sql_msg1.find('INSERT 0 3') > -1)
        logger.info('------3.查看表中数据，返回信息被加密-----')
        sql_cmd2 = 'select address from table001 where name=\'lucy\';'
        sql_msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        logger.info(sql_msg2)
        sql_msg2_list = sql_msg2.splitlines()
        self.assertTrue(sql_msg2_list[0].strip() == 'address' and
                        sql_msg2_list[2].strip() != 'shanxi.xian,yantaqu0569-5'
                        and sql_msg2_list[-1].strip() == '(1 row)')
        logger.info('------4.加密查询出来的结果，作为查询条件查询表数据-----')
        sql_cmd3 = f'select name from table001 where ' \
                   f'address=\'{sql_msg2_list[2].strip()}\';'
        sql_msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.common.equal_sql_mdg(sql_msg3, 'name', 'lucy', '(1 row)',
                                  flag='1')
        logger.info('------5.将解密查询出来的结果，作为查询条件查询表数据-----')
        sql_cmd4 = f'select address from table001 where address=' \
                   f'gs_decrypt(\'{sql_msg2_list[2].strip()}\',' \
                   f'\'QAZ2wssx@123\',\'sm4\');'
        sql_msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        self.common.equal_sql_mdg(sql_msg4, 'address',
                                  'shanxi.xian,yantaqu0569-5',
                                  '(1 row)', flag='1')
        logger.info('------6.查看审计日志，检查步骤2-5中语句的信息是否记录正确-----')
        sleep(5)
        end_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        end_time = end_time_msg.splitlines()[2].strip()
        sql_cmd4 = f'select * from pg_query_audit(\'{start_time}\',' \
                   f'\'{end_time}\');'
        sql_msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        logger.info(sql_msg4)
        self.assertTrue('select address from table001 where '
                        'address=gs_decrypt(********)' in sql_msg4 and
                        'insert into table001 values(\'lucy\','
                        'gs_encrypt(********)')
        logger.info('-----7.查看po_log日志，检查步骤2-5中语句的信息是否记录正确-----')
        shell_cmd5 = f'ls -t {self.logfile_name} | head -1'
        logger.info(shell_cmd5)
        log_name = os.path.join(self.logfile_name, self.userNode.sh(
            shell_cmd5).result())
        logger.info(log_name)
        shell_cmd6 = f'cat {log_name} |grep \'select address from table001 ' \
                     f'where address\';' \
                     f'cat {log_name} |grep \'insert into table001 values\''
        content_msg = self.userNode.sh(shell_cmd6).result()
        logger.info(content_msg)
        self.assertTrue('select address from table001 where '
                        'address=gs_decrypt(********)' in sql_msg4 and
                        'insert into table001 values(\'lucy\','
                        'gs_encrypt(********)')

    def tearDown(self):
        logger.info('-------1.清理表------')
        sql_cmd1 = 'drop table table001;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertTrue(msg1.find('DROP TABLE') > -1)
        logger.info('-------2.恢复参数配置------')
        exe_cmd2 = f'source {self.DB_ENV_PATH};' \
                   f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
                   f'"audit_dml_state_select={int(return_msg1)}";'
        logger.info(exe_cmd2)
        msg2 = self.userNode.sh(exe_cmd2).result()
        logger.info(msg2)
        sql_cmd3 = 'show audit_dml_state_select;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        self.common.equal_sql_mdg(msg3, 'audit_dml_state_select',
                                  f'{return_msg1}', '(1 row)', flag='1')
        exe_cmd4 = f'source {self.DB_ENV_PATH};' \
                   f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
                   f'"audit_dml_state={int(return_msg2)}";'
        logger.info(exe_cmd4)
        msg4 = self.userNode.sh(exe_cmd4).result()
        logger.info(msg4)
        sql_cmd5 = 'show audit_dml_state;'
        msg5 = self.sh_primy.execut_db_sql(sql_cmd5)
        logger.info(msg5)
        self.common.equal_sql_mdg(msg5, 'audit_dml_state', f'{return_msg2}',
                                  '(1 row)', flag='1')
        exe_cmd6 = f'source {self.DB_ENV_PATH};' \
                   f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
                   f'"log_statement={return_msg3}";'
        logger.info(exe_cmd6)
        msg6 = self.userNode.sh(exe_cmd6).result()
        logger.info(msg6)
        sql_cmd7 = 'show log_statement;'
        msg7 = self.sh_primy.execut_db_sql(sql_cmd7)
        logger.info(msg7)
        self.common.equal_sql_mdg(msg7, 'log_statement', f'{return_msg3}',
                                  '(1 row)', flag='1')
        logger.info('----Opengauss_Function_Security_sm4_Case0001 finish----')
