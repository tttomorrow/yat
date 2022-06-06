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
Case Type   : GUC
Case Name   : 修改enable_wdr_snapshot为on，观察预期结果；
Description :
    1、查询enable_wdr_snapshot默认值；
    show enable_wdr_snapshot;
    2、修改enable_wdr_snapshot为on，重启使其生效，并校验其预期结果；
    gs_guc set -D {cluster/dn1} -c "enable_wdr_snapshot=on"
    gs_guc set -D {cluster/dn1} -c "wdr_snapshot_interval=10"
    gs_om -t stop && gs_om -t start
    show enable_wdr_snapshot;
    3、10min后查询快照生成
    4、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改成功，校验修改后系统参数值为on；
    3、10min后查询快照生成+1
    4、恢复默认值成功；
History     :
"""
import os
import time
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class PerformanceShot(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info("==Opengauss_Function_Guc_Performance_Shot_Case0001"
                         "开始执行==")
        self.constant = Constant()
        self.common = Common()
        self.primary_sh = CommonSH("PrimaryDbUser")
        self.user_node = Node('PrimaryDbUser')
        is_started = self.primary_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)

        self.db_name = "postgres"

        text = "备份pg_hba.conf文件"
        self.logger.info(text)
        self.hba = os.path.join(macro.DB_INSTANCE_PATH, "pg_hba.conf")
        result = self.common.get_sh_result(self.user_node,
                                           f"cp {self.hba} {self.hba}backup")
        self.assertNotIn("bash", result, "执行失败:" + text)
        self.assertNotIn("ERROR", result, "执行失败:" + text)

    def test_snapshot(self):
        text = "--step1:查询enable_wdr_snapshot;expaect:默认值off"
        self.logger.info(text)
        result = self.primary_sh.execut_db_sql("show enable_wdr_snapshot;")
        self.logger.info(result)
        self.assertIn("off", result, "执行失败:" + text)
        result = self.primary_sh.execut_db_sql("show wdr_snapshot_interval;")
        self.logger.info(result)
        self.assertIn("1h", result, "执行失败:" + text)

        result = "select count(*) from snapshot.snapshot;"
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gsql -d {self.db_name} -p {self.user_node.db_port} -c "{result}"
            '''
        self.logger.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        self.logger.info(msg)
        if self.constant.NOT_EXIST in msg:
            shot_num1 = 0
        else:
            shot_num1 = msg.split("\n")[-2].strip()

        text = "修改pg_hba文件;expect:设置成功"
        self.logger.info(text)
        self.logger.info("查询目标行号")
        info = "Unix domain socket connections"
        cmd = f"cat {self.hba}| grep -n '{info}'"
        self.logger.info(cmd)
        result = self.common.get_sh_result(self.user_node, cmd)
        self.logger.info(result)
        self.assertNotIn("bash", result, "执行失败:" + text)
        num = int(result.split(':')[0])
        num += 1
        self.logger.info(num)
        self.logger.info("添加主机trust信息")
        hba_info = f"host all all {self.user_node.ssh_host}/32 trust"
        self.logger.info(hba_info)
        cmd = f"sed -i '{num}a {hba_info}' {self.hba}"
        self.logger.info(cmd)
        result = self.common.get_sh_result(self.user_node, cmd)
        self.logger.info(result)
        self.assertNotIn("bash", result, "执行失败:" + text)

        self.logger.info("现存pg_hba文件信息")
        cmd = f"cat {self.hba}| tail -n +{num}"
        self.logger.info(cmd)
        result = self.common.get_sh_result(self.user_node, cmd)
        self.logger.info(result)
        self.primary_sh.restart_db_cluster()
        is_started = self.primary_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)

        text = "--step2:方式一修改enable_wdr_snapshot为on重启使其生效;expect:设置成功"
        self.logger.info(text)
        res = self.primary_sh.execute_gsguc("set",
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            "enable_wdr_snapshot=on")
        self.assertTrue(res, "执行失败:" + text)
        self.logger.info("方式一修改wdr_snapshot_interval为10min"
                         "重启使其生效，期望：设置成功")
        res = self.primary_sh.execute_gsguc("set",
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            "wdr_snapshot_interval=10")
        self.assertTrue(result, "执行失败:" + text)

        self.logger.info("期望：重启后查询结果为on")
        self.logger.info("期望：重启后查询结果为10min")
        self.primary_sh.restart_db_cluster()
        status = self.primary_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        result = self.primary_sh.execut_db_sql("show enable_wdr_snapshot;")
        self.logger.info(result)
        self.assertIn("on", result, "执行失败:" + text)
        result = self.primary_sh.execut_db_sql("show wdr_snapshot_interval;")
        self.logger.info(result)
        self.assertIn("10min", result, "执行失败:" + text)

        self.logger.info("查询最新快照生成时间")
        sql = "select start_ts from snapshot.snapshot " \
              "order by start_ts desc limit 1;"
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gsql -d {self.db_name} -p {self.user_node.db_port} -c "{sql}"
            '''
        self.logger.info(excute_cmd)
        start_ts1 = self.user_node.sh(excute_cmd).result()
        self.logger.info(start_ts1)
        start_ts1 = start_ts1.split("\n")[-2].strip().split(".")[0]
        self.logger.info(start_ts1)

        text = "--step3:等待10min后查询;expect:快照生成+1"
        self.logger.info(text)
        time.sleep(630)
        sql = "select count(*) from snapshot.snapshot;"
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gsql -d {self.db_name} -p {self.user_node.db_port} -c "{sql}"
            '''
        self.logger.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        self.logger.info(msg)
        shot_num2 = msg.split("\n")[-2].strip()

        self.logger.info("10min后查询最新快照生成时间")
        sql = "select start_ts from snapshot.snapshot " \
              "order by start_ts desc limit 1;"
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gsql -d {self.db_name} -p {self.user_node.db_port} -c "{sql}"
            '''
        self.logger.info(excute_cmd)
        result = self.user_node.sh(excute_cmd).result()
        self.logger.info(result)
        start_ts2 = result.split("\n")[-2].strip().split(".")[0]
        self.logger.info(start_ts2)

        self.logger.info("断言快照10min生成1个")
        self.assertGreater(int(shot_num2), int(shot_num1), "执行失败:" + text)
        self.logger.info("断言快照生成间隔时间为10min")
        result = self.primary_sh.execut_db_sql(f"select date '{start_ts2}' - "
                                               f"date '{start_ts1}';")
        self.logger.info(result)
        self.assertEqual('10', result.split("\n")[-2].strip().split(':')[1],
                         "执行失败:" + text)

    def tearDown(self):
        text = "--step4:恢复默认值;expect:恢复成功"
        self.logger.info(text)
        self.logger.info("恢复pg_hba.conf文件")
        self.hba = os.path.join(macro.DB_INSTANCE_PATH, "pg_hba.conf")
        mv_result = self.common.get_sh_result(self.user_node,
                                           f"mv {self.hba}backup {self.hba}")
        self.logger.info(mv_result)
        self.primary_sh.execute_gsguc("set",
                                             self.constant.GSGUC_SUCCESS_MSG,
                                             "enable_wdr_snapshot=off")
        self.primary_sh.execute_gsguc("set",
                                             self.constant.GSGUC_SUCCESS_MSG,
                                             "wdr_snapshot_interval=60")
        self.primary_sh.restart_db_cluster()
        is_started = self.primary_sh.get_db_cluster_status()

        res1 = self.primary_sh.execut_db_sql("show enable_wdr_snapshot;")
        self.logger.info(res1)
        res2 = self.primary_sh.execut_db_sql("show wdr_snapshot_interval;")
        self.logger.info(res2)

        self.assertIn("off", res1, "执行失败:" + text)
        self.assertIn("1h", res2, "执行失败:" + text)
        self.assertEqual("", mv_result, "执行失败:" + text)
        self.assertTrue("Degraded" in is_started or "Normal" in is_started,
                        "执行失败:" + text)
        self.logger.info("==Opengauss_Function_Guc_Performance_Shot_Case0001"
                         "执行结束==")
