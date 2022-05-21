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
Case Type   : Postgis
Case Name   : 拷贝postgis相关动态库和配置文件适配功能
Description :
    1、拷贝postgis相关动态库和配置文件至对应路径下
    2、连接数据库，创建扩展
Expect      :
    1、相应文件拷贝成功
    2、连接数据库成功，创建扩展成功
History     :
"""

import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Logger import Logger


class PostgisTest(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.common = Common()
        self.sh_primysh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.constant = Constant()
        self.file_path1 = os.path.join(macro.DB_INSTANCE_PATH, '../app/lib')
        self.file_path2 = os.path.join(macro.DB_INSTANCE_PATH,
                                       '../app/share/postgresql/extension')
        self.file_path3 = os.path.join(self.file_path1, 'postgresql')

        platform = ['x86_64', 'aarch64']
        cmd = 'arch'
        res = self.user_node.sh(cmd).result()
        self.src_file_path = macro.POSTGIS_URL_X86 if res.strip() == platform[
            0] else macro.POSTGIS_URL_ARM
        self.log.info(self.src_file_path)

    def test_postgis(self):
        self.log.info('------Opengauss_Function_Postgis_Case0001开始执行------')

        file_list = ['libjson-c.so.2', 'libgeos_c.so.1', 'libproj.so.9',
                     'libgeos-3.6.2.so', 'libgdal.so.1.18.0',
                     'liblwgeom-2.4.so.0', 'postgis.control',
                     'postgis--2.4.2.sql', 'postgis_raster--2.4.2.sql',
                     'postgis_raster.control', 'postgis_topology--2.4.2.sql',
                     'postgis_topology.control', 'postgis-2.4.so']

        text = '---step1:拷贝相关动态库和配置文件到数据库对应路径下   expect:成功---'
        self.log.info(text)

        for file in file_list[0:6]:
            text = f'---copy {file}文件---'
            self.log.info(text)
            copy_cmd1 = f'wget -P {self.file_path1} \
                {self.src_file_path}/{file};'
            self.log.info(copy_cmd1)

            copy_res1 = self.user_node.sh(copy_cmd1).result()
            self.log.info(copy_res1)

            cat_cmd1 = f'ls {self.file_path1} | grep {file}'
            self.log.info(cat_cmd1)

            cat_res1 = self.user_node.sh(cat_cmd1).result()
            self.log.info(cat_res1)
            self.assertIn(file, cat_res1, '执行失败' + text)

        text = '---预置条件，清理对应目录下文件---'
        self.log.info(text)
        rm_cmd = f'rm -rf {self.file_path2}/postgis_raster--2.*.sql' \
            f'rm -rf {self.file_path2}/postgis_topology--2.*.sql'
        self.log.info(rm_cmd)
        rm_res = self.user_node.sh(rm_cmd).result()
        self.log.info(rm_res)
        self.assertNotIn('bash', rm_res)

        for file in file_list[6:12]:
            text = f'---copy {file}文件---'
            self.log.info(text)
            copy_cmd2 = f'wget -P {self.file_path2} \
                {self.src_file_path}/{file};'
            self.log.info(copy_cmd2)

            copy_res2 = self.user_node.sh(copy_cmd2).result()
            self.log.info(copy_res2)

            cat_cmd2 = f'ls {self.file_path2} | grep {file}'
            self.log.info(cat_cmd2)

            cat_res2 = self.user_node.sh(cat_cmd2).result()
            self.log.info(cat_res2)
            self.assertIn(file, cat_res2, '执行失败' + text)

        text = '---copy postgis-2.4.so文件---'
        self.log.info(text)
        copy_cmd3 = f'wget -P {self.file_path3} \
            {self.src_file_path}/{file_list[-1]};'
        self.log.info(copy_cmd3)

        copy_res3 = self.user_node.sh(copy_cmd3).result()
        self.log.info(copy_res3)

        cat_cmd3 = f'ls {self.file_path3} | grep {file_list[-1]}'
        self.log.info(cat_cmd3)

        cat_res3 = self.user_node.sh(cat_cmd3).result()
        self.log.info(cat_res3)
        self.assertIn(file_list[-1], cat_res3, '执行失败' + text)

        text = '---step2:创建extension;   expect:成功---'
        self.log.info(text)
        sql_cmd = 'drop extension if exists postgis cascade;' \
                  'create extension postgis;'
        self.log.info(sql_cmd)

        sql_res = self.sh_primysh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        self.assertIn('CREATE EXTENSION', sql_res)

    def tearDown(self):
        self.log.info('------No need to clean------')
        self.log.info('------Opengauss_Function_Postgis_Case0001执行结束------')
