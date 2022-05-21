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
Case Type   : 基础功能
Case Name   : recovery_target_inclusive为true时，设置recovery_target_xid恢复
Description :
    1.主节点开启归档
    2.创建表
    3.备份
    4、再次插入数据,按如下顺序开启多个session
    5.破坏数据库
    6.恢复数据到step4中查询的xid节点
    7.重启数据库
    8.查询数据库恢复情况
    9、查看数据库状态
Expect      :
    1、成功
    2、成功
    3、成功
    4、成功
    5、成功
    6、成功
    7、成功
    8、recovery.conf文件变成revocery.done；
    9、数据库最终可退出恢复状态
History     :
    file changed as we read it,修改备份方式规避该问题
"""
import unittest
import os
import time
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.ComThread import ComThread


class Pitrclass(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info("--------Opengauss_Function_PITR_Case0010 start-------")
        self.constant = Constant()
        self.commonshpri = CommonSH('PrimaryDbUser')
        self.parent_path = os.path.dirname(macro.DB_INSTANCE_PATH)
        self.archive = os.path.join(self.parent_path, 'archive_backup')
        self.primary_user_node = Node(node='PrimaryDbUser')
        self.tbname = 't_pitr_case0010'
        result = self.commonshpri.get_db_cluster_status('detail')
        self.log.info(result)
        self.node_num = result.count('Standby Normal') + 1
        self.comshsta = []
        self.archive_status = \
            os.path.join(macro.DB_INSTANCE_PATH, 'pg_xlog', 'archive_status')
        self.flg = True

        self.hostname = self.primary_user_node.sh("hostname").result()
        self.log.info(f"hostname is {self.hostname}")
        self.nodelist = ['Standby1DbUser', 'Standby2DbUser']
        self.backup_path = os.path.join(self.parent_path, 'backup_pitr')

    def test_backup0026(self):
        text = '--step1:主节点开启归档 expect:成功--'
        self.log.info(text)
        cmd = f"cp " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'postgresql.conf')} " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'postgresql.confbak')}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        result = self.commonshpri.execute_gsguc(
            "reload", self.constant.GSGUC_SUCCESS_MSG,
            "archive_mode = on", self.hostname)
        self.assertTrue(result, '执行失败:' + text)
        cmd = f"mkdir {self.archive}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        result = self.commonshpri.execute_gsguc(
            "reload", self.constant.GSGUC_SUCCESS_MSG,
            f"archive_command = 'cp %p {self.archive}/%f'", self.hostname)
        self.assertTrue(result, '执行失败:' + text)

        text = '----step2: 创建表 expect:成功----'
        self.log.info(text)
        cmd = f"create table {self.tbname}(i int, xid varchar(100), " \
            f"c varchar(1000),time timestamp);" \
            f"INSERT INTO {self.tbname} VALUES(0, " \
            f"txid_current(), 'before backup', now());"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, result,
                      '执行失败:' + text)

        text = '-------step3:备份  expect:成功---------'
        self.log.info(text)
        time.sleep(10)
        cmd = f"mkdir {self.backup_path}"
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertEqual('', result, '执行失败:' + text)
        result = self.commonshpri.exec_gs_basebackup(
            self.backup_path, self.primary_user_node.db_host,
            self.primary_user_node.db_port)
        self.assertTrue(result, '执行失败:' + text)
        cmd = f"chmod 700 {self.backup_path}"
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)

        text = '----step4: 再次插入数据,按如下顺序开启多个session expect:成功----'
        self.log.info(text)
        session_thread = []
        cmd = f"insert into {self.tbname} " \
            f"values(1,txid_current(), 'after backup', now());" \
            f"select pg_switch_xlog();"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn('INSERT', result, '执行失败:' + text)
        cmd = f"begin;" \
            f"insert into {self.tbname} " \
            f"values(2,txid_current(), 'transcation A begin...', now());" \
            f"select pg_sleep(10);" \
            f"insert into {self.tbname} " \
            f"values(7,txid_current(), 'transcation A commit...', now());" \
            f"end;"
        session_thread.append(
            ComThread(self.commonshpri.execut_db_sql, args=(cmd, '')))
        session_thread[0].setDaemon(True)
        session_thread[0].start()
        time.sleep(1)
        cmd = f"begin;" \
            f"insert into {self.tbname} " \
            f"values(3,txid_current(), 'transcation B begin...', now());" \
            f"select pg_sleep(30);" \
            f"insert into {self.tbname} " \
            f"values(11,txid_current(), 'transcation B commit...', now());"\
            f"end;"
        session_thread.append(
            ComThread(self.commonshpri.execut_db_sql, args=(cmd, '')))
        session_thread[1].setDaemon(True)
        session_thread[1].start()
        time.sleep(1)
        cmd = f"begin;" \
            f"insert into {self.tbname} " \
            f"values(4,txid_current(), 'transcation test begin...', now());" \
            f"select pg_sleep(20);" \
            f"insert into {self.tbname} " \
            f"values(9,txid_current(), 'transcation test commit...', now());"\
            f"end;"
        session_thread.append(
            ComThread(self.commonshpri.execut_db_sql, args=(cmd, '')))
        session_thread[2].setDaemon(True)
        session_thread[2].start()
        time.sleep(1)
        cmd = f"begin;" \
            f"insert into {self.tbname} " \
            f"values(5,txid_current(), 'transcation C begin...', now());" \
            f"select pg_sleep(15);" \
            f"insert into {self.tbname} " \
            f"values(8,txid_current(), 'transcation C commit...', now());"\
            f"end;"
        session_thread.append(
            ComThread(self.commonshpri.execut_db_sql, args=(cmd, '')))
        session_thread[3].setDaemon(True)
        session_thread[3].start()
        time.sleep(1)
        cmd = f"begin;" \
            f"insert into {self.tbname} " \
            f"values(6,txid_current(), 'transcation D begin...', now());" \
            f"select pg_sleep(25);" \
            f"insert into {self.tbname} " \
            f"values(10,txid_current(), 'transcation D commit...', now());"\
            f"end;"
        session_thread.append(
            ComThread(self.commonshpri.execut_db_sql, args=(cmd, '')))
        session_thread[4].setDaemon(True)
        session_thread[4].start()
        for i in range(5):
            session_thread[i].join(50)
            result = session_thread[i].get_result()
            self.log.info(result)
            self.assertIn('COMMIT', result, '执行失败:' + text)
        cmd = f"select * from {self.tbname} order by i;"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn("12 rows", result, '执行失败:' + text)
        self.xid = result.splitlines()[6].split('|')[1].strip()
        self.log.info(self.xid)

        cmd = f"ls -al {self.archive_status}"
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)

        cmd = f"ls -al {self.archive}"
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)

        text = '----step7: 破坏数据库 expect:成功----'
        self.log.info(text)
        result = self.commonshpri.stop_db_cluster()
        self.assertTrue(result, '执行失败:' + text)
        time.sleep(3)
        cmd = f"rm -rf {macro.DB_INSTANCE_PATH}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)

        text = '----step8: 恢复数据到step4中查询的xid节点 expect:成功----'
        self.log.info(text)
        cmd = f"mv {self.backup_path} {macro.DB_INSTANCE_PATH}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)

        cmd = f"ls {os.path.join(macro.DB_INSTANCE_PATH, 'pg_xlog')} " \
            f"-alI '*.backup'"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.xlog = result.splitlines()[3].split(' ')[-1]
        self.log.info(self.xlog)
        cmd = f"mv " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_xlog', self.xlog)} " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_xlog', 'xlogbak')};" \
            f"rm -rf {os.path.join(macro.DB_INSTANCE_PATH, 'pg_xlog')}/0*;" \
            f"rm -rf " \
            f"{self.archive_status}/*;" \
            f"mv " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_xlog', 'xlogbak')} " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_xlog', self.xlog)};" \
            f"ls -al {os.path.join(macro.DB_INSTANCE_PATH, 'pg_xlog')};" \
            f"ls -al {self.archive_status}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        cmd = f"touch " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'recovery.conf')};" \
            f"echo \"restore_command = 'cp {self.archive}/%f %p'\" > " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'recovery.conf')};" \
            f"echo \"recovery_target_xid='{self.xid}'\" >> " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'recovery.conf')};" \
            f"echo \"recovery_target_inclusive=true\" >> " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'recovery.conf')};" \
            f"cat {os.path.join(macro.DB_INSTANCE_PATH, 'recovery.conf')};"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)

        text = '----step9: 重启数据库 expect:成功----'
        self.log.info(text)
        result = self.commonshpri.start_db_cluster(True)
        flg = 'Degraded' in result or \
              self.constant.START_SUCCESS_MSG in result
        self.assertTrue(flg, '执行失败:' + text)

        text = '----step10: 查询数据库恢复情况 ' \
               'expect:recovery.conf文件变成revocery.done；----'
        self.log.info(text)
        cmd = f"select * from {self.tbname} order by i;"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertNotIn('transcation B begin...', result, '执行失败:' + text)
        self.assertNotIn('transcation D begin...', result, '执行失败:' + text)
        self.assertNotIn('transcation D commit...', result, '执行失败:' + text)
        self.assertNotIn('transcation B commit...', result, '执行失败:' + text)
        self.assertIn('8 rows', result, '执行失败:' + text)
        self.log.info(text)
        time.sleep(30)
        cmd_1 = f"select pg_is_in_recovery();"
        status_result = self.commonshpri.execut_db_sql(cmd_1)
        self.log.info(status_result)
        time.sleep(5)
        if 't' in status_result.splitlines()[-2]:
            cmd = "select pg_xlog_replay_resume();"
            result = self.commonshpri.execut_db_sql(cmd)
            self.log.info(result)
            time.sleep(60)
            cmd = "select pg_is_in_recovery();"
            result = self.commonshpri.execut_db_sql(cmd)
            self.log.info(result)
            self.assertIn('f', result.splitlines()[-2], '执行失败:' + text)
        else:
            self.assertIn('f', status_result.splitlines()[-2], '执行失败:' + text)
        self.flg = False
        cmd = f"ls -al  {macro.DB_INSTANCE_PATH}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn('recovery.done', result, '执行失败:' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('------------------清理环境-------------')
        result = self.commonshpri.get_db_cluster_status('status')
        if not result or self.flg:
            cmd = f'''if [ -d "{self.backup_path}" ]
                      then
                          rm -rf {macro.DB_INSTANCE_PATH};
                          mv {self.backup_path} {macro.DB_INSTANCE_PATH}
                       fi'''
            self.log.info(cmd)
            result = self.primary_user_node.sh(cmd).result()
            self.log.info(result)
            self.commonshpri.start_db_cluster()
        for i in range(int(self.node_num) - 1):
            self.comshsta.append(CommonSH(self.nodelist[i]))
            self.comshsta[i].build_standby("-t 3600")
        cmd = f"yes | mv " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'postgresql.confbak')} " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'postgresql.conf')}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.commonshpri.stop_db_cluster()
        self.commonshpri.start_db_cluster()
        cmd = f"drop table if exists {self.tbname};"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        cmd = f"rm -rf {os.path.join(self.parent_path, 'data.tar')};" \
            f"rm -rf {self.archive};" \
            f"rm -rf {os.path.join(macro.DB_INSTANCE_PATH, 'recovery*')}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.log.info("-Opengauss_Function_PITR_Case0010 end-")
