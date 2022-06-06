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
Case Name   : enable_global_syscache参数设置为on，对应系统函数、视图查询功能验证
Description :
    0、查看enable_global_syscache初始配置值;
    1、修改参数enable_global_syscache为on;
    2、重启数据库，使参数生效;
    3、查询gsc相关系统函数、视图;
    3.1、查询gs_gsc_memory_detail;
    3.2、查询gs_lsc_memory_detail;
    3.3、查询gs_gsc_dbstat_info;
    3.4、查询gs_gsc_table_detail;
    3.5、查询gs_gsc_catalog_detail;
    3.6、查询gs_gsc_clean;
Expect      :
    0、查看enable_global_syscache初始配置值;
    1、修改参数enable_global_syscache为on; 修改成功
    2、重启数据库，使参数生效; 重启成功
    3、查询gsc相关系统函数、视图;
    3.1、查询gs_gsc_memory_detail; 查询结果不为空
    3.2、查询gs_lsc_memory_detail; 查询结果不为空
    3.3、查询gs_gsc_dbstat_info; 查询结果不为空
    3.4、查询gs_gsc_table_detail; 查询结果不为空
    3.5、查询gs_gsc_catalog_detail; 查询结果不为空
    3.6、查询gs_gsc_clean; 查询结果为t
History     :
"""
import os
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class GscTestCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'----{os.path.basename(__file__)}:start----')
        self.sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.com = Common()
        step_txt = '----step0:查看enable_global_syscache初始配置值;----'
        self.log.info(step_txt)
        self.init_para = self.com.show_param("enable_global_syscache")

    def test_main(self):
        step_txt = '----step1:修改参数enable_global_syscache为on; expect:修改成功----'
        self.log.info(step_txt)
        msg = self.sh.execute_gsguc('set',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"enable_global_syscache= on")
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----step2:重启数据库，使参数生效; expect:重启成功----'
        self.log.info(step_txt)
        restart_result = self.sh.restart_db_cluster()
        self.assertTrue(restart_result)
        self.log.info('----查询参数----')
        self.new_para = self.com.show_param("enable_global_syscache")
        self.assertEqual(self.new_para, 'on', '执行失败:' + step_txt)

        step_txt = '----step3:查询gsc相关系统函数、视图;----'
        self.log.info(step_txt)
        step_txt = '----step3.1:查询gs_gsc_memory_detail; expect:查询结果不为空----'
        self.log.info(step_txt)
        select_result = self.check_select('gs_gsc_memory_detail')
        self.assertGreater(select_result, 0, '执行失败:' + step_txt)

        step_txt = '----step3.2:查询gs_lsc_memory_detail; expect:查询结果不为空----'
        self.log.info(step_txt)
        select_result = self.check_select('gs_lsc_memory_detail')
        self.assertGreater(select_result, 0, '执行失败:' + step_txt)

        step_txt = '----step3.3:查询gs_gsc_dbstat_info; expect:查询结果不为空----'
        self.log.info(step_txt)
        select_result = self.check_select('gs_gsc_dbstat_info()')
        self.assertGreater(select_result, 0, '执行失败:' + step_txt)

        step_txt = '----step3.4:查询gs_gsc_table_detail; expect:查询结果不为空----'
        self.log.info(step_txt)
        select_result = self.check_select('gs_gsc_table_detail()')
        self.assertGreater(select_result, 0, '执行失败:' + step_txt)

        step_txt = '----step3.5:查询gs_gsc_catalog_detail; expect:查询结果不为空----'
        self.log.info(step_txt)
        select_result = self.check_select('gs_gsc_catalog_detail()')
        self.assertGreater(select_result, 0, '执行失败:' + step_txt)

        step_txt = '----step3.6:查询gs_gsc_clean; expect:查询结果为t----'
        self.log.info(step_txt)
        select_result = self.check_select('gs_gsc_clean()', False)
        self.assertEqual(select_result.splitlines()[-2].strip().lower(), 't',
                         '执行失败:' + step_txt)

        step_txt = '----step4:查询数据库状态; expect:状态正常----'
        self.log.info(step_txt)
        status_result = self.sh.get_db_cluster_status('status')
        self.assertTrue(status_result, '执行失败:' + step_txt)

    def check_select(self, object_name, is_select_count=True):
        """
        :param object_name: 查询对象名称
        :param is_select_count: 查询count还是所有结果
        :return: 查询结果count数或查询结果
        """
        if is_select_count:
            select_sql1 = f'select count(*) from {object_name};'
            select_result = self.sh.execut_db_sql(select_sql1)
            self.log.info(select_result)
            select_result = int(select_result.splitlines()[-2].strip())
        else:
            select_sql1 = f'select * from {object_name};'
            select_result = self.sh.execut_db_sql(select_sql1)
            self.log.info(select_result)
        return select_result

    def tearDown(self):
        step_txt = '----this is teardown----'
        self.log.info(step_txt)
        step1_txt = '----还原参数enable_global_syscache为初始值; expect:修改成功----'
        self.log.info(step1_txt)
        msg = self.sh.execute_gsguc('set',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"enable_global_syscache="
                                    f"{self.init_para}")
        step2_txt = '----重启数据库，使参数生效; expect:重启成功----'
        self.log.info(step2_txt)
        restart_result = self.sh.restart_db_cluster()

        self.log.info(f'----{os.path.basename(__file__)}:end----')
        self.assertTrue(msg, '执行失败:' + step_txt + step1_txt)
        self.assertTrue(restart_result, '执行失败:' + step_txt + step2_txt)
