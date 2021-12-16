"""
Case Type   : 功能测试
Case Name   : 创建一个Data Source对象，含TYPE, VERSION, OPTIONS
Description :
    1. 先使用gs_guc工具生成datasource.key.cipher和datasource.key.rand文件
        并使用gs_ssh工具发布到openGauss每个节点的$GAUSSHOME/bin目录
    2. 创建Data Source对象，含TYPE, VERSION, OPTIONS
        username/password不包含'encryptOpt'前缀
    3. 查询创建的数据源对象信息
    4. 删除数据源对象
    5. 删除文件
Expect      :
    1.gs命令执行成功，文件生成
    2.数据源对象创建成功
    3.系统表PG_EXTENSION_DATA_SOURCE显示数据源的名称，类型，版本等信息
    4.删除数据源对象成功
    5.文件删除成功
History     : 
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.user = Node('dbuser')
        self.commonsh = CommonSH('dbuser')
        self.env = macro.DB_ENV_PATH
        self.dn1 = macro.DB_INSTANCE_PATH
        self.pwd = macro.COMMON_PASSWD
        self.log.info("Opengauss_Function_DDL_Create_DataSource_Case0009开始")

    def test_data_source(self):
        self.cluster = self.dn1.rstrip('dn1')
        cmd0 = f'cd {self.cluster};ls'
        msg0 = self.user.sh(cmd0).result()
        files = msg0.splitlines()
        folder = [i for i in files if i.strip().startswith('app_')][0]
        self.path = os.path.join(self.cluster, f'{folder}/bin')
        self.file1 = os.path.join(self.path, 'datasource.key.cipher')
        self.file2 = os.path.join(self.path, 'datasource.key.rand')
        cmd2 = f'rm -rf {self.file1};rm -rf {self.file2}'
        self.user.sh(cmd2).result()

        self.log.info("通过明文密码生自定义的test.key.cipher和test.key.rand文件")
        cmd = f'''source {self.env};gs_ssh -c\
            "gs_guc generate -S {self.pwd} -D {self.path} -o datasource"
            '''
        self.log.info(cmd)
        msg1 = self.user.sh(cmd).result()
        self.log.info(msg1)
        self.assertIn('Successfully', msg1)

        self.data_source = ['boy', 'ds____2', '___9ds3']
        user = ['yestertodayoncemore', '____$98765',
                '987654321234567890wishuhaveahappynewyearandalwaysbe']
        pswd = user
        for i in range(3):
            cmd1 = f'''drop data source if exists {self.data_source[i]};
                create data source {self.data_source[i]} type 'unknown' 
                version '11.2.3' 
                options (dsn 'heyboy', username '{user[i]}',
                password '{pswd[i]}', encoding '');
                '''
            msg1 = self.commonsh.execut_db_sql(cmd1)
            self.log.info(msg1)
            self.assertTrue('CREATE DATA SOURCE' in msg1)
            cmd2 = f'''select srcname, srctype, srcversion, srcacl, srcoptions 
                from PG_EXTENSION_DATA_SOURCE 
                where srcname = '{self.data_source[i]}';
                '''
            msg2 = self.commonsh.execut_db_sql(cmd2)
            self.log.info(msg2)
            res = msg2.split('\n')[2].split('|')
            res_ds = res[0].strip()
            res_version = res[2].strip()
            res_dsn = res[-1].split(',')[-4]
            res_usr = res[-1].split(',')[-3]
            res_pwd = res[-1].split(',')[-2]
            self.assertTrue(res_ds == self.data_source[i])
            self.assertTrue(res_version == '11.2.3')
            self.assertTrue(res_dsn.strip() == '{dsn=' + 'heyboy')
            self.assertTrue(res_usr.startswith('username=encryptOpt'))
            self.assertTrue(user[i] not in res_usr and len(res_usr) > 50)
            self.assertTrue(res_pwd.startswith('password=encryptOpt'))
            self.assertTrue(pswd[i] not in res_pwd and len(res_pwd) > 50)

    def tearDown(self):
        for i in range(3):
            cmd = f'drop data source if exists {self.data_source[i]};'
            self.commonsh.execut_db_sql(cmd)
        cmd2 = f'''source {self.env};\
            gs_ssh -c "rm -rf {self.file1};rm -rf {self.file2}"'''
        msg2 = self.user.sh(cmd2).result()
        self.log.info(msg2)
        self.log.info("Opengauss_Function_DDL_Create_DataSource_Case0009结束")