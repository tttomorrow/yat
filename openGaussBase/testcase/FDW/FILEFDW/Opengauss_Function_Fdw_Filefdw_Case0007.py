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
Case Type   : file_fdw功能
Case Name   : file_fdw外表option参数escape功能验证
Description :
    1、新建文件如下：
        0,column2,column3
        1,test1,-test1\test-
        2,test2,-test2\\test-
        3,test3,-test3@-test-
    2、创建服务
    3、创建外表(指定escape为\，指定quote为-)，查询外表数据
    4、修改外表escape为'@'，查询外表数据
    5、修改文件为
        0,column,column3
        7,test7,-test7--test-
    6、修改外表escape为-（quote与escape相等），查询外表数据
Expect      :
    1、新建文件成功
    2、创建服务成功
    3、创建外表(指定escape为\，指定quote为-)成功，查询外表数据'\'正常转义,'@'无法转义
    4、修改外表escape为'@'，查询外表数据，'@'正常转义
    ERROR:  unterminated CSV quoted field
    5、修改文件成功
    6、修改外表escape为-（quote与escape相等）成功，查询外表数据'-'正常转义
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Filefdw0007(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Fdw_Filefdw_Case0007:初始化----')
        self.dbUserNode = Node(node='dbuser')
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.file_name = 'file_fdwCase0007.csv'
        self.file_path = os.path.join(macro.DB_BACKUP_PATH, self.file_name)
        self.tb_name = 't_filefdw0007'
        self.svc_name = 'svc_filefdw_0007'
        self.err_flag = 'ERROR:  unterminated CSV quoted field'

    def test_main(self):
        step_txt = '----step1: 数据库用户创建文件; expect:创建成功----'
        self.log.info(step_txt)
        file_content = '0,column2,column3\n' \
                       '1,test1,-test1\\1-\n' \
                       '2,test2,-test2\\\\\\2-\n' \
                       '3,test3,-test3@-3-'
        write_cmd = f"echo -e '{file_content}' > {self.file_path}"
        self.log.info(write_cmd)
        self.pri_dbuser.sh(write_cmd).result()
        file_exist = f'cat {self.file_path}'
        self.log.info(file_exist)
        file_cat = self.pri_dbuser.sh(file_exist).result()
        self.log.info(file_cat)
        real_content = '0,column2,column3\n' \
                       '1,test1,-test1\\1-\n' \
                       '2,test2,-test2\\\\2-\n' \
                       '3,test3,-test3@-3-'
        self.log.info(real_content)
        self.assertEqual(real_content, file_cat, '执行失败:' + step_txt)

        step_txt = '----step2: 创建服务; expect:创建成功----'
        self.log.info(step_txt)
        sql = f"drop server {self.svc_name} cascade;" \
            f"create server {self.svc_name} foreign data wrapper file_fdw;"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn("CREATE SERVER", result, "执行失败" + step_txt)

        step_txt = r'----step3: 创建外表(指定escape为\，指定quote为-); expect:创建成功----'
        self.log.info(step_txt)
        sql = f"create foreign table {self.tb_name} " \
            f"(column1 int,column2 char(20),column3 char(20)) " \
            f"server {self.svc_name} options (filename '{self.file_path}'," \
            f"format 'csv', header 'true' ,escape '\\',quote '-');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, result,
                      "执行失败" + step_txt)
        step_txt = r'----step3: 查询外表数据; expect:查询外表数据\正常转义----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name} limit 2;"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(r'test2\2', result, "执行失败" + step_txt)
        step_txt = '----step3: 查询外表数据; expect:@不能转义----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name} where column1 = 3;"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.err_flag, result, "执行失败" + step_txt)

        step_txt = '----step4: 修改外表escape为@;expect:成功----'
        self.log.info(step_txt)
        sql = f"alter foreign table {self.tb_name} options (set escape '@');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertEqual("ALTER FOREIGN TABLE", result, "执行失败" + step_txt)
        step_txt = '----step4: 查询外表数据; expect:@正常转义;----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('test3-3', result, "执行失败" + step_txt)

        step_txt = '----step5: 修改文件内容;expect:成功----'
        self.log.info(step_txt)
        file_content = '0,column,column3\n' \
                       '7,test7,-test7--test-'
        write_cmd = f"echo -e '{file_content}' > {self.file_path}"
        self.log.info(write_cmd)
        self.pri_dbuser.sh(write_cmd).result()
        file_exist = f'cat {self.file_path}'
        self.log.info(file_exist)
        file_cat = self.pri_dbuser.sh(file_exist).result()
        self.log.info(file_cat)
        self.assertEqual(file_content, file_cat, '执行失败:' + step_txt)

        step_txt = '----step6: 修改外表escape为（quote与escape相等）为-; expect:修改成功----'
        self.log.info(step_txt)
        sql = f"alter foreign table {self.tb_name} options (set escape '-');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertEqual("ALTER FOREIGN TABLE", result, "执行失败" + step_txt)
        step_txt = '----step6: 查询外表数据（quote与escape相等）为-; expect:-正常转义----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('test7-test', result, '执行失败:' + step_txt)

    def tearDown(self):
        self.log.info('----this is tearDown----')
        step_txt = '----step7:清理数据----'
        self.log.info(step_txt)
        drop_sql = f"drop foreign table if exists {self.tb_name};" \
            f"drop server {self.svc_name} cascade;"
        result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(result)

        step_txt = '----step8:删除文件----'
        self.log.info(step_txt)
        file_rm_cmd = f'rm -rf  {self.file_path};ls -al {self.file_path}'
        self.log.info(file_rm_cmd)
        file_rm_result = self.pri_dbuser.sh(file_rm_cmd).result()
        self.log.info(file_rm_result)

        self.log.info('----Opengauss_Function_Fdw_Filefdw_Case0007:执行完毕----')
