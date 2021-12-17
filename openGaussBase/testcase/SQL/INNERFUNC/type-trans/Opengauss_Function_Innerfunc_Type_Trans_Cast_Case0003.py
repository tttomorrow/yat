"""
Case Type   : 功能测试
Case Name   : cast函数将字符串类型转换为二进制类型
Description :
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.入参是符合转换的类型
    步骤 3.类型与指定不符、不能转换、未指定类型等异常校验
Expect      : 
    步骤 1：数据库状态正常
    步骤 2：成功转换为二进制类型
    步骤 3：合理报错
History     : 
"""
import unittest
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class Cast_function(unittest.TestCase):

    def setUp(self):
        logger.info("--------Opengauss_Function_Innerfunc_Type_Trans_Cast_Case0003开始执行------------")
        self.commonsh = CommonSH('dbuser')

    def test_function(self):
        logger.info("-------------合法及非法入参转换校验------------")

        sql_list = [r"""SELECT CAST('\xdeadbeef'::varchar as BYTEA);""",
                    r"""SELECT CAST('5ff' as RAW);""",
                    r"""SELECT CAST(lpad('1',24,'101') as BLOB);""",
                    r"""SELECT CAST('\xdeadbeef'::int4 as BYTEA);""",
                    r"""SELECT CAST('x5ff' as RAW);""",
                    r"""SELECT CAST(lpad('1','101') as BLOB);"""]

        result_list = ['\\xdeadbeef', '05FF', '101101101101101101101101']
        for i in range(6):
            msg = self.commonsh.execut_db_sql(sql_list[i])
            logger.info(msg)
            if i < 3:
                self.assertTrue(msg.splitlines()[2].strip() == result_list[i])
            else:
                self.assertTrue('ERROR:  invalid' in msg)

    def tearDown(self):
        logger.info('----------Opengauss_Function_Innerfunc_Type_Trans_Cast_Case0003执行结束---------')