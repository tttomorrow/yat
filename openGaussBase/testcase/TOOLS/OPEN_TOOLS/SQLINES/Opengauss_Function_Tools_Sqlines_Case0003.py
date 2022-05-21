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
Case Type   : sqlines工具
Case Name   : sqlines工具-s参数值大小写混用
Description :
    1、安装sqlines
    2、创建测试脚本
    3、sqlines -s=poStgresql -t=opengauss -in={self.in_file}
       -out={self.out_file} -log={self.log_file}
    4、sqlines -s=oRacle -t=opengauss -in={self.in_file} -out={self.out_file}
        -log={self.log_file}
    5、sqlines -s=mYsQl -t=opengauss -in={self.in_file} -out={self.out_file}
        -log={self.log_file}
    6、环境清理：卸载sqlines、删除对应文件
Expect      :
    1、sqlines安装成功
    2、脚本创建成功
    3、转换成功
    4、转换成功
    5、转换成功
    6、环境清理成功
History     :
"""

import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger


class SqlinesTest(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info(f'----- {os.path.basename(__file__)} start-----')
        self.root = Node('PrimaryRoot')
        self.in_file = 'Opengauss_Function_Tools_Sqlines_Case0003.sql'
        self.out_file = 'Opengauss_Function_Tools_Sqlines_Case0003_out.sql'
        self.log_file = 'Opengauss_Function_Tools_Sqlines_Case0003.log'

    def test_main(self):
        step_txt = '----step1:安装sqlines，expect: sqlines安装成功----'
        self.log.info(step_txt)
        self.log.info('-------------------下载软件包--------------------')
        self.file_name = 'openGauss-tools-sqlines-master.zip'
        file_download = os.path.join(os.path.dirname(macro.FTP_PATH),
                                     'sqlines', self.file_name)
        cmd = f'wget {file_download}'
        self.log.info(cmd)
        self.root.sh(cmd)
        cmd2 = f'ls {self.file_name}'
        self.log.info(cmd2)
        res = self.root.sh(cmd2).result()
        self.log.info(res)
        self.assertEqual(self.file_name, res, '文件下载失败：' + step_txt)

        self.log.info('-------------------解压软件包--------------------')
        cmd3 = f'unzip {self.file_name}'
        self.log.info(cmd3)
        res = self.root.sh(cmd3).result()
        self.log.info(res)
        self.unzip_dir = self.file_name.replace('.zip', '')
        cmd4 = f'ls -d {self.unzip_dir}'
        self.log.info(cmd4)
        res = self.root.sh(cmd4).result()
        self.log.info(res)
        self.assertEqual(self.unzip_dir, res, '文件解压失败：' + step_txt)

        self.log.info('-------------------安装sqlines--------------------')
        cmd = f'cd {self.unzip_dir};sh build.sh -i;pwd'
        self.log.info(cmd)
        res = self.root.sh(cmd).result()
        self.log.info(res)
        self.assertIn('Install Sqlines successfully', res,
                      'Sqlines安装失败：' + step_txt)
        tmp_path = res.strip().splitlines()[-1].strip()
        mid_path = os.path.join(tmp_path, 'bin')
        file_name = 'sqlines'
        check_file = os.path.join(mid_path, file_name)
        cmd = f"ls -l {check_file}"
        self.log.info(cmd)
        res = self.root.sh(cmd).result()
        self.log.info(res)
        self.assertEqual(res[3], 'x', '文件没有执行权限' + step_txt)
        self.log.info('-----------------配置sqlines环境变量-----------------')
        self.source_path = f"export PATH={mid_path}:$PATH"

        step_txt = '----step2:创建测试脚本，expect: 脚本创建成功----'
        self.log.info(step_txt)
        cmd1 = f"""cat >{self.in_file} <<EOF
        create table Sqlines_Case0003(id int);
        """
        self.log.info(cmd1)
        self.root.sh(cmd1)
        cmd2 = f'ls {self.in_file}'
        self.log.info(cmd2)
        res = self.root.sh(cmd2).result()
        self.log.info(res)
        self.assertEqual(res, f'{self.in_file}', '执行失败' + step_txt)

        step_txt = '----step3:执行sqlines命令，expect: 转换成功不报错----'
        self.log.info(step_txt)
        cmd = f"{self.source_path};" \
            f"sqlines -s=poStgresql -t=opengauss -in={self.in_file} " \
            f"-out={self.out_file} -log={self.log_file}"
        self.log.info(cmd)
        res = self.root.sh(cmd).result()
        self.log.info(res)
        self.assertNotIn('error', res, '执行失败：')

        step_txt = '----step4:执行sqlines命令，expect: 转换成功不报错----'
        self.log.info(step_txt)
        cmd = f"{self.source_path};" \
            f"sqlines -s=oRacle -t=opengauss -in={self.in_file} " \
            f"-out={self.out_file} -log={self.log_file}"
        self.log.info(cmd)
        res = self.root.sh(cmd).result()
        self.log.info(res)
        self.assertNotIn('error', res, '执行失败：')

        step_txt = '----step5:执行sqlines命令，expect: 转换成功不报错----'
        self.log.info(step_txt)
        cmd = f"{self.source_path};" \
            f"sqlines -s=mYsQl -t=opengauss -in={self.in_file} " \
            f"-out={self.out_file} -log={self.log_file}"
        self.log.info(cmd)
        res = self.root.sh(cmd).result()
        self.log.info(res)
        self.assertNotIn('error', res, '执行失败：')

    def tearDown(self):
        step_txt = '----step6:环境清理，expect: 环境清理成功----'
        self.log.info(step_txt)
        self.log.info('--------------------卸载sqlines--------------------')
        cmd = f'cd {self.unzip_dir};sh build.sh -m'
        self.log.info(cmd)
        res = self.root.sh(cmd).result()
        self.log.info(res)
        self.log.info('--------------------删除相关文件--------------------')
        cmd = f"rm -rf {self.file_name} {self.unzip_dir} sqlines.log " \
            f"{self.in_file} {self.out_file} {self.log_file}"
        self.log.info(cmd)
        self.root.sh(cmd)
        self.assertIn('Uninstall Sqlines successfully', res,
                      'Sqlines卸载失败：' + step_txt)
        self.log.info(f'----- {os.path.basename(__file__)} end-----')
