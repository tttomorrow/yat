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
Case Name   : 订阅发布创建1w个表
Description :
    1.在两个集群创建表相同结构1w个表
    2.创建发布端
    3.创建订阅
    4.修改表数据
    5.查询是否同步
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
    5.同步
History     :
"""
import unittest
import os
import time
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(3 != Primary_SH.get_node_num(), '非1+2环境不执行')
class Pubsubclass(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} start-----")
        self.pri_userdb_list = [
            Node(node='PrimaryDbUser'), 
            Node(node='remote1_PrimaryDbUser')]
        self.constant = Constant()
        self.commsh_pub = CommonSH('PrimaryDbUser')
        self.commsh_sub = CommonSH('remote1_PrimaryDbUser')
        self.com_pub = Common()
        self.tb_name = 'tb_pubsub_case124'
        self.subname = "sub_case124"
        self.pubname = "pub_case124"
        self.parent_path_pub = os.path.dirname(macro.DB_INSTANCE_PATH)
        self.parent_path_sub = os.path.dirname(macro.DB_INSTANCE_PATH_REMOTE1)
        self.port = str(int(self.pri_userdb_list[0].db_port) + 1)
        self.wal_level = self.com_pub.show_param("wal_level")
        self.user_param_pub = f'-U {self.pri_userdb_list[0].db_user} ' \
            f'-W {self.pri_userdb_list[0].db_password}'
        self.user_param_sub = f'-U {self.pri_userdb_list[1].db_user} ' \
            f'-W {self.pri_userdb_list[1].db_password}'

        cmd = f"cp " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')} " \
            f"{os.path.join(self.parent_path_pub, 'pg_hba.conf')};"
        self.log.info(cmd)
        result = self.pri_userdb_list[0].sh(cmd).result()
        self.log.info(result)
        cmd = f"cp " \
            f"{os.path.join(macro.DB_INSTANCE_PATH_REMOTE1, 'pg_hba.conf')}" \
            f" {os.path.join(self.parent_path_sub, 'pg_hba.conf')};"
        self.log.info(cmd)
        result = self.pri_userdb_list[1].sh(cmd).result()
        self.log.info(result)
        self.tb_num = 10000
        self.div = 20
        self.file_path_list = [
            os.path.join(self.parent_path_pub, 'file_pub_sub_case124'), 
            os.path.join(self.parent_path_sub, 'file_pub_sub_case124')]
        self.create_path_list = [
            os.path.join(self.file_path_list[0], 'create'),
            os.path.join(self.file_path_list[1], 'create')]
        self.drop_path_list = [
            os.path.join(self.file_path_list[0], 'drop'),
            os.path.join(self.file_path_list[1], 'drop')]
        self.insert_path_list = [
            os.path.join(self.file_path_list[0], 'insert'),
            os.path.join(self.file_path_list[1], 'insert')]
        self.select_path_list = [
            os.path.join(self.file_path_list[0], 'select'),
            os.path.join(self.file_path_list[1], 'select')]
        self.sh_path_list = [
            os.path.join(self.file_path_list[0], 'execute.sh'), 
            os.path.join(self.file_path_list[1], 'execute.sh')]
        self.div_num = int(self.tb_num/self.div)

    def test_pubsub(self):
        text = '--step:预置条件,修改pg_hba expect:成功'
        self.log.info(text)
        tb_struct = f"create table {self.tb_name}_\$i" \
            f"( iggggggggggggggggggggggggggggg1 int primary key, " \
            f"iggggggggggggggggggggggggggggggg2 point, " \
            f"iggggggggggggggggggggg3 lseg, " \
            f"igggggggggggggggggggggg4 box, " \
            f"igggggggggggggggggggggggggggggggggggggggggggggggggggggg5" \
            f" path,igggggggggggggggggggggggggggggggggggggggggggggggggg6" \
            f" path,i7 polygon,i8 circle, i9 bit(3),i10 bit varying(5)," \
            f"icccccccccccccccccccccccccccc11 DATE," \
            f"i12 TIME  WITHOUT TIME ZONE,i13 TIME WITH TIME ZONE, " \
            f"i14 TIMESTAMP WITHOUT TIME ZONE,i15 TIMESTAMP WITH  " \
            f"TIME ZONE,i16 SMALLDATETIME, i1ddddddddd6 INTERVAL DAY(3)" \
            f"  TO SECOND (4),i17 interval year (6), " \
            f"idddddddddddddddddddddddd18 date, " \
            f"iffffffffffffffffffffff19 timestamp, " \
            f"iccccccccccccccccccccccccccccc20 timestamp, " \
            f"iffffffffffffffffffffff21 date, irrrrrrrrrrrrrrrr22 " \
            f"date, idddddddddddddddddddddddddd23 date, " \
            f"issssssss24 date,i25 time, i26 int, i27 int,  " \
            f"ilonglong_____________________________________" \
            f"__________________________28 int, i29 int, i30 int, " \
            f"i31 int,  i32 int, i33 int,i34 int, i35 text, i36 text," \
            f"i37 text, i38 text, i39 text, i40 text, i41 text, " \
            f"i42 text,  i43 BOOLEAN,i44 BOOLEAN,i45 BOOLEAN," \
            f"i46 BOOLEAN, i47 BOOLEAN,i48 BOOLEAN," \
            f"i49 BOOLEAN,i50 BOOLEAN);"
        insert_values = f"insert into {self.tb_name}_\$i " \
            f"values(1, point'2,3'," \
            f"lseg'[(1,2),(2,2)]',box'(2,4),(4,4)'," \
            f"path'((1,2),(1,3),(3,2),(3,3))',path'[(1,1),(1,2),(1,3)]'," \
            f"polygon'(1,2),(1,3),(3,2),(3,3)',circle'4,4,2', B'101'," \
            f"B'00', '2021-12-15','21:21:21','21:21:21 pst'," \
            f"'2010-12-12','2013-12-11 pst'," \
            f"'2003-04-12 04:05:06',INTERVAL '3' DAY," \
            f"interval '2' year,'2021-12-15','today','now'," \
            f"'now','tomorrow','epoch','epoch','allballs',26,27,28,29," \
            f"30,31,32,33,34,'35','36','37','38','39','40','41','42'," \
            f"True,True,True,True,False,False,False,False);"
        for i_idx in range(2):
            cmd = f"mkdir -p {self.file_path_list[i_idx]} &&" \
                f"touch {self.sh_path_list[i_idx]}; "
            self.log.info(cmd)
            result = self.pri_userdb_list[i_idx].sh(cmd).result()
            self.log.info(result)
            for idx in range(self.div):
                cmd = f"touch {self.create_path_list[i_idx]}{idx}.sql;" \
                    f"touch {self.insert_path_list[i_idx]}{idx}.sql;" \
                    f"touch {self.select_path_list[i_idx]}{idx}.sql;" \
                    f"touch {self.drop_path_list[i_idx]}{idx}.sql;"
                self.log.info(cmd)
                result = self.pri_userdb_list[i_idx].sh(cmd).result()
                self.log.info(result)
                cmd = f'echo "for ((i={idx}*{self.div_num};' \
                    f'i<{idx}*{self.div_num}+{self.div_num};i++))">>' \
                    f'{self.sh_path_list[i_idx]};' \
                    f'echo "do">>{self.sh_path_list[i_idx]};' \
                    f'echo "echo \\\"{tb_struct}\\\">>' \
                    f'{self.create_path_list[i_idx]}{idx}.sql">>' \
                    f'{self.sh_path_list[i_idx]};' \
                    f'echo "echo \\\"{insert_values}\\\">>' \
                    f'{self.insert_path_list[i_idx]}{idx}.sql">>' \
                    f'{self.sh_path_list[i_idx]};' \
                    f'echo "echo \\\"select * ' \
                    f'from {self.tb_name}_\$i;\\\">>' \
                    f'{self.select_path_list[i_idx]}{idx}.sql">>' \
                    f'{self.sh_path_list[i_idx]};' \
                    f'echo "echo \\\"drop table {self.tb_name}_\$i;\\\">>' \
                    f'{self.drop_path_list[i_idx]}{idx}.sql">>' \
                    f'{self.sh_path_list[i_idx]};' \
                    f'echo "done">>{self.sh_path_list[i_idx]};'
                self.log.info(cmd)
                result = self.pri_userdb_list[i_idx].sh(cmd).result()
                self.log.info(result)
            cmd = f'sh {self.sh_path_list[i_idx]};'
            self.log.info(cmd)
            result = self.pri_userdb_list[i_idx].sh(cmd).result()
            self.log.info(result)
        self.log.info("###########发布端：")
        guc_res = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, '',
            f'host    replication  {self.pri_userdb_list[1].db_user} '
            f'{self.pri_userdb_list[1].db_host}/32 sha256')
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG, 'wal_level=logical')
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_pub.restart_db_cluster(True)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)
        self.log.info("###########订阅端：")
        guc_res = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host    replication  {self.pri_userdb_list[0].db_user} '
            f'{self.pri_userdb_list[0].db_host}/32 sha256',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)

        text = '--step1:在两个集群创建表相同结构1w个表 expect:成功--'
        self.log.info(text)
        for idx in range(self.div):
            cmd = f"source {macro.DB_ENV_PATH};" \
                f"gsql -p{self.pri_userdb_list[0].db_port} " \
                f"-d{self.pri_userdb_list[0].db_name} " \
                f"-f {self.create_path_list[0]}{idx}.sql " \
                f"{self.user_param_pub}"
            result = self.pri_userdb_list[0].sh(cmd).result()
            self.log.info(result)
            self.assertIn(self.constant.TABLE_CREATE_SUCCESS,
                          result, '执行失败:' + text)
            self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                             '执行失败:' + text)
            cmd = f"source {macro.DB_ENV_PATH_REMOTE1};" \
                f"gsql -p{self.pri_userdb_list[1].db_port} " \
                f"-d{self.pri_userdb_list[1].db_name} " \
                f"-f {self.create_path_list[1]}{idx}.sql " \
                f"{self.user_param_sub}"
            result = self.pri_userdb_list[1].sh(cmd).result()
            self.log.info(result)
            self.assertIn(self.constant.TABLE_CREATE_SUCCESS,
                          result, '执行失败:' + text)
            self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                             '执行失败:' + text)
            time.sleep(5)

        text = '--step2:创建发布端 expect:成功--'
        self.log.info(text)
        sql = f"CREATE PUBLICATION {self.pubname}  FOR  all TABLEs;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.create_pub_succ_msg, result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)

        text = '--step3:创建订阅 expect:成功--'
        self.log.info(text)
        result = self.commsh_sub.execute_generate(
            macro.COMMON_PASSWD, env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertIn('', result, '执行失败:' + text)
        sql = f"CREATE SUBSCRIPTION {self.subname} CONNECTION " \
            f"'host={self.pri_userdb_list[0].db_host} " \
            f"port={self.port} " \
            f"user={self.pri_userdb_list[0].db_user} " \
            f"dbname={self.pri_userdb_list[0].db_name} " \
            f"password={self.pri_userdb_list[0].ssh_password}' " \
            f"PUBLICATION {self.pubname}"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.create_sub_succ_msg,
                      result, '执行失败:' + text)

        text = '--step4:修改表数据 expect:成功--'
        self.log.info(text)
        for idx in range(self.div):
            cmd = f"source {macro.DB_ENV_PATH};" \
                f"gsql -p{self.pri_userdb_list[0].db_port} " \
                f"-d{self.pri_userdb_list[0].db_name} " \
                f"-f {self.insert_path_list[0]}{idx}.sql " \
                f"{self.user_param_pub}"
            result = self.pri_userdb_list[0].sh(cmd).result()
            self.log.info(result)
            self.assertIn(self.constant.INSERT_SUCCESS_MSG,
                          result, '执行失败' + text)
            self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                             '执行失败:' + text)
            time.sleep(30)

        text = "--step5:查询是否同步 expect:数据同步--"
        self.log.info(text)
        for idx in range(self.div):
            cmd = f"source {macro.DB_ENV_PATH};" \
                f"gsql -p{self.pri_userdb_list[0].db_port} " \
                f"-d{self.pri_userdb_list[0].db_name} " \
                f"-f {self.select_path_list[0]}{idx}.sql " \
                f"{self.user_param_pub}"
            result_p = self.pri_userdb_list[0].sh(cmd).result()
            self.log.info("###########发布端结果：")
            self.log.info(result_p)
            time.sleep(20)
            cmd = f"source {macro.DB_ENV_PATH_REMOTE1};" \
                f"gsql -p{self.pri_userdb_list[1].db_port} " \
                f"-d{self.pri_userdb_list[1].db_name} " \
                f"-f {self.select_path_list[1]}{idx}.sql " \
                f"{self.user_param_sub}"
            result = self.pri_userdb_list[1].sh(cmd).result()
            self.log.info("###########订阅端结果：")
            self.log.info(result)
            self.assertEqual(result.splitlines()[:-2],
                             result_p.splitlines()[:-2], '执行失败:' + text)
            self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                             '执行失败:' + text)
            time.sleep(20)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = '--清理环境--'
        self.log.info(text)
        sql = f"DROP PUBLICATION if exists {self.pubname};"
        drop_pub_result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(drop_pub_result)
        sql = f"DROP SUBSCRIPTION  {self.subname};"
        drop_sub_result = self.commsh_sub.execut_db_sql(
            sql, self.user_param_sub, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(drop_sub_result)
        for idx in range(self.div):
            cmd = f"source {macro.DB_ENV_PATH};" \
                f"gsql -p{self.pri_userdb_list[0].db_port} " \
                f"-d{self.pri_userdb_list[0].db_name} " \
                f"-f {self.drop_path_list[0]}{idx}.sql " \
                f"{self.user_param_pub}"
            result = self.pri_userdb_list[0].sh(cmd).result()
            self.log.info(result)
            cmd = f"source {macro.DB_ENV_PATH_REMOTE1};" \
                f"gsql -p{self.pri_userdb_list[1].db_port} " \
                f"-d{self.pri_userdb_list[1].db_name} " \
                f"-f {self.drop_path_list[1]}{idx}.sql " \
                f"{self.user_param_sub}"
            result = self.pri_userdb_list[1].sh(cmd).result()
            self.log.info(result)
            time.sleep(5)
        cmd = f"mv " \
            f"{os.path.join(self.parent_path_pub, 'pg_hba.conf')} "\
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')};" \
            f"rm -rf {self.file_path_list[0]}"
        self.log.info(cmd)
        result = self.pri_userdb_list[0].sh(cmd).result()
        self.log.info(result)
        cmd = f"mv " \
            f"{os.path.join(self.parent_path_sub, 'pg_hba.conf')} "\
            f"{os.path.join(macro.DB_INSTANCE_PATH_REMOTE1, 'pg_hba.conf')};" \
            f"rm -rf {self.file_path_list[1]};"
        self.log.info(cmd)
        result = self.pri_userdb_list[1].sh(cmd).result()
        self.log.info(result)
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'wal_level={self.wal_level}')
        self.assertTrue(result, '执行失败:' + text)
        self.commsh_pub.restart_db_cluster(True)
        self.commsh_sub.restart_db_cluster(True, macro.DB_ENV_PATH_REMOTE1)
        self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                      '执行失败' + text)
        self.assertIn(self.constant.drop_sub_succ_msg, drop_sub_result,
                      '执行失败' + text)
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} end-----")
