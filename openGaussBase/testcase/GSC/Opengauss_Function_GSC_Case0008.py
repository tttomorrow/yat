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
Case Type   : GSC功能模块
Case Name   : global_syscache_threshold内存阈值设置验证
Description :
    1、查询global_syscache_threshold默认参数值
    2、修改global_syscache_threshold为上限值1024GB并查询
    3、修改global_syscache_threshold为下限值16MB并查询
    4、修改global_syscache_threshold为20480kB并查询
    5、修改global_syscache_threshold为不带单位并查询
    6、修改global_syscache_threshold为默认值并查询
    7、alter system方式修改global_syscache_threshold;
Expect      :
    1、查询global_syscache_threshold默认参数值为160M
    2、修改global_syscache_threshold为上限值1024GB并查询，修改正确
    3、修改global_syscache_threshold为下限值16MB并查询，修改正确
    4、修改global_syscache_threshold为20480kB并查询，修改正确
    5、修改global_syscache_threshold为不带单位并查询，修改正确
    6、修改global_syscache_threshold为默认值并查询，修改正确
    7、alter system方式修改global_syscache_threshold;修改正确
History     :
"""
import os
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class GscTestCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'----{os.path.basename(__file__)}:start----')
        self.sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.com = Common()
        self.pri_dbuser = Node(node='PrimaryDbUser')

    def test_main(self):
        step_txt = '----step1:查看global_syscache_threshold初始值;' \
                   'expect:结果为160MB----'
        self.log.info(step_txt)
        self.init_para = self.com.show_param('global_syscache_threshold')
        self.assertEqual(self.init_para, '160MB', '执行失败:' + step_txt)

        step_txt = '----step2:修改global_syscache_threshold为上限值1024GB并查询; ' \
                   'expect:修改正确----'
        self.log.info(step_txt)
        msg = self.sh.execute_gsguc('reload',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"global_syscache_threshold= 1024GB")
        self.assertTrue(msg, '执行失败:' + step_txt)
        new_para = self.com.show_param('global_syscache_threshold')
        self.assertEqual(new_para, '1024GB', '执行失败:' + step_txt)

        step_txt = '----step3:修改global_syscache_threshold为下限值16MB并查询; ' \
                   'expect:修改正确----'
        self.log.info(step_txt)
        msg = self.sh.execute_gsguc('reload',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"global_syscache_threshold= 16MB")
        self.assertTrue(msg, '执行失败:' + step_txt)
        new_para = self.com.show_param('global_syscache_threshold')
        self.assertEqual(new_para, '16MB', '执行失败:' + step_txt)

        step_txt = '----step4:修改global_syscache_threshold为20480kB并查询; ' \
                   'expect:修改正确----'
        self.log.info(step_txt)
        msg = self.sh.execute_gsguc('reload',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"global_syscache_threshold= 20480kB")
        self.assertTrue(msg, '执行失败:' + step_txt)
        new_para = self.com.show_param('global_syscache_threshold')
        self.assertEqual(new_para, '20MB', '执行失败:' + step_txt)

        step_txt = '----step5:修改global_syscache_threshold为不带单位并查询; ' \
                   'expect:修改正确----'
        self.log.info(step_txt)
        msg = self.sh.execute_gsguc('reload',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"global_syscache_threshold= 20480")
        self.assertTrue(msg, '执行失败:' + step_txt)
        new_para = self.com.show_param('global_syscache_threshold')
        self.assertEqual(new_para, '20MB', '执行失败:' + step_txt)

        step_txt = '----step6:修改global_syscache_threshold为默认值并查询; ' \
                   'expect:修改正确----'
        self.log.info(step_txt)
        msg = self.sh.execute_gsguc('reload',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"global_syscache_threshold")
        self.assertTrue(msg, '执行失败:' + step_txt)
        new_para = self.com.show_param('global_syscache_threshold')
        self.assertEqual(new_para, self.init_para, '执行失败:' + step_txt)

        step_txt = '----step7:alter system方式修改global_syscache_threshold; ' \
                   'expect:修改正确----'
        self.log.info(step_txt)
        alter_sql = "alter system set global_syscache_threshold to '30720MB';"
        result = self.sh.execut_db_sql(alter_sql)
        self.log.info(result)
        self.assertIn(self.constant.alter_system_success_msg, result,
                      '执行失败:' + step_txt)
        new_para = self.com.show_param('global_syscache_threshold')
        self.assertEqual(new_para, '30GB', '执行失败:' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step_txt = '----修改global_syscache_threshold为初始值并查询; ' \
                   'expect:设置成功----'
        self.log.info(step_txt)
        msg = self.sh.execute_gsguc('reload',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"global_syscache_threshold="
                                    f"{self.init_para}")
        new_para = self.com.show_param('global_syscache_threshold')

        self.log.info(f'----{os.path.basename(__file__)}:end----')
        self.assertTrue(msg, '执行失败:' + step_txt)
        self.assertEqual(new_para, self.init_para, '执行失败:' + step_txt)
