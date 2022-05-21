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
Case Type   : 系统内部使用工具
Case Name   : 指定--external-mapping与--tablespace-mapping一起使用，
              --tablespace-mapping=OLDDIR=NEWDIR 选项中含有“=”，
              使用反斜杠转义后执行restore
Description :
    1.新建目录
    2.创建表空间及表
    3.进行初始化
    4.在备份路径内初始化一个新的备份实例
    5.进行全量备份
    6.执行restore
    7.删除新建目录,恢复集群状态
Expect      :
    1.新建目录成功
    2.创建表空间与表成功
    3.进行初始化成功
    4.在备份路径内初始化一个新的备份实例成功
    5.进行备份成功
    6.停止集群成功，restore成功
    7.删除新建目录成功,集群状态恢复成功
History     :
"""

import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from yat.test import Node
from yat.test import macro

LOG = Logger()


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('-------------------this is setup--------------------')
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0081开始执行-')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('---------step1 新建文件与备份目录--------------')
        instance_path = f'{macro.DB_INSTANCE_PATH}'
        LOG.info('实例路径为：' + instance_path)
        index1 = instance_path.find('/')
        index2 = instance_path.rfind('/')
        self.cluster_path = instance_path[index1:index2]
        LOG.info(self.cluster_path)
        mkdir_cmd = f"mkdir {self.cluster_path}/testdir;" \
            f"mkdir {self.cluster_path}/prodir;" \
            f"mkdir {self.cluster_path}/aaa;" \
            f"mkdir {self.cluster_path}/bb=b;" \
            f"ls {self.cluster_path};" \
            f"touch {self.cluster_path}/aaa/a.dat;" \
            f"echo 'this is test file' >> {self.cluster_path}/aaa/a.dat;"
        LOG.info(mkdir_cmd)
        mkdir_msg = self.PrimaryNode.sh(mkdir_cmd).result()
        LOG.info(mkdir_msg)
        self.assertTrue(
            'testdir' and 'prodir' and 'aaa' and 'bb=b' in mkdir_msg)

        LOG.info('---------step2 创建表空间及表--------------')
        create_msg = self.sh_primary.execut_db_sql(
            "create tablespace tbs_backup1 location "
            f"'{self.cluster_path}/aaa';"
            "create table table_backup1 (a int) tablespace tbs_backup1;"
            "insert into table_backup1 values (8);")
        LOG.info(create_msg)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, create_msg)

        LOG.info('----------step3 进行初始化------------------')
        init_cmd = f"source {macro.DB_ENV_PATH};gs_probackup init -B " \
            f"{self.cluster_path}/testdir;"
        LOG.info(init_cmd)
        init_msg = self.PrimaryNode.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertIn(self.constant.init_success, init_msg)

        LOG.info('-----step4 在备份路径内初始化一个新的备份实例---')
        init_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup add-instance -B {self.cluster_path}/testdir " \
            f"-D {macro.DB_INSTANCE_PATH} --instance=pro1 ;"
        LOG.info(init_cmd)
        init_msg = self.PrimaryNode.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertIn("'pro1' " + self.constant.init_success, init_msg)

        LOG.info('-------------step5 执行全量备份---------------')
        back_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup backup -B {self.cluster_path}/testdir " \
            f" --instance=pro1 -b full  -d {self.PrimaryNode.db_name} -p " \
            f"{self.PrimaryNode.db_port} --external-dirs" \
            f"={self.cluster_path}/aaa:{self.cluster_path}/bb\\=b;"
        LOG.info(back_cmd)
        back_msg = self.PrimaryNode.sh(back_cmd).result()
        LOG.info(back_msg)
        self.assertIn('completed', back_msg)
        self.backupmsg = back_msg.splitlines()[-1]
        LOG.info(self.backupmsg)
        self.backupid = self.backupmsg.split()[2]
        LOG.info('备份ID为：' + self.backupid)

        LOG.info('-----------step6.1 执行restore--------------')
        restore_cmd = f"source {macro.DB_ENV_PATH};" \
            f"cd {self.cluster_path} ;" \
            f"gs_probackup restore -B {self.cluster_path}/testdir " \
            f"-D {self.cluster_path}/prodir --instance=pro1  " \
            f"-i {self.backupid} --external-mapping=" \
            f"{self.cluster_path}/aaa={self.cluster_path}/bb\\\=b " \
            f"--tablespace-mapping={self.cluster_path}/aaa" \
            f"={self.cluster_path}/bb\\\=b ;"
        LOG.info(restore_cmd)
        restore_msg = self.PrimaryNode.sh(restore_cmd).result()
        LOG.info(restore_msg)
        self.assertIn(f'Restore of backup {self.backupid} completed',
                      restore_msg)

        LOG.info('----------step6.2 查看还原后的表空间目录---------------')
        check_cmd = f"ls " \
            f"{self.cluster_path}/bb=b ;"
        LOG.info(check_cmd)
        check_msg = self.PrimaryNode.sh(check_cmd).result()
        LOG.info(check_msg)
        self.assertIn('a.dat', check_msg)

    def tearDown(self):
        LOG.info('------------------this is tearDown----------------------')
        LOG.info('------------------step7.1 删除表和表空间----------------')
        create_msg = self.sh_primary.execut_db_sql(
            "drop table table_backup1 ;"
            "drop tablespace tbs_backup1 ;")
        LOG.info(create_msg)
        LOG.info('-----------------step7.2 删除新建目录------------------')
        clear_cmd = f"rm -rf {self.cluster_path}/testdir;" \
            f"rm -rf {self.cluster_path}/prodir;" \
            f"rm -rf {self.cluster_path}/aaa;" \
            f"rm -rf {self.cluster_path}/bb=b;" \
            f"rm -rf {self.cluster_path}/bbb;"
        LOG.info(clear_cmd)
        clear_msg = self.PrimaryNode.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0081执行完成-')
