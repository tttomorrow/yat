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
Case Type   : 功能测试
Case Name   : 验证表空间属性maxsize
Description :
    1.新建表空间space2，设置size为1K
    2.新建表tb2，插入大小为736K的数据，修改其所属表空间为space2
    3.创建表空间space1，设置size为1K
    4.创建表tb1,指定表空间为space1，插入大于1K数据
    5.修改表空间space1的size为10240K（10M）
    6.插入大小为736K的数据
    7.修改表空间space1的size为1K
Expect      : 
    1.创建成功
    2.提示超出限额大小
    3.修改成功
    4.插入失败
    5.修改成功
    6.插入成功
    7.提示超出限额大小（目前是修改成功）
History     : 
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

log = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        log.info("--Opengauss_Function_DDL_Tablespace_Case0012开始--")
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_tablespace(self):
        error_info = "ERROR:  Insufficient storage space for tablespace"
        self.drop = f"""drop table if exists tb1;
            drop table if exists tb2;
            drop tablespace if exists space1;
            drop tablespace if exists space2;"""
        msg = self.commonsh.execut_db_sql(self.drop)
        log.info(msg)
        log.info('----创建两个大小为1K的表空间----')
        self.create_space = f"""create tablespace space1 relative 
            location 'tablespace/path1' maxsize '1K';
            create tablespace space2 relative location 
            'tablespace/path2' maxsize '1K';"""
        msg = self.commonsh.execut_db_sql(self.create_space)
        log.info(msg)

        log.info('------测试点1:已有表大小超过表空间大小，不能指定表空间-------')
        cmd0 = """create table tb2(id int);
            insert into tb2 values(generate_series(1,20000));
            alter table tb2 set tablespace space2;"""
        msg0 = self.commonsh.execut_db_sql(cmd0)
        log.info(msg0)
        self.assertTrue(error_info in msg0)

        log.info('------测试点2:插入表数据大小超过其表空间大小，不能插入------')
        log.info('------创建表tb1指定表空间为space1，插入大于1K数据------')
        cmd1 = f"""create table tb1(id int) tablespace space1;
            insert into tb1 values(generate_series(1,20000));"""
        msg1 = self.commonsh.execut_db_sql(cmd1)
        log.info(msg1)
        self.assertTrue(error_info in msg1)

        log.info('------测试点3:插入表数据大小不超过其表空间大小，插入成功------')
        log.info('------修改表空间space1的size为10240K(10M)------')
        cmd2 = f"""alter tablespace space1 resize maxsize '10240K';
            select spcmaxsize from pg_tablespace where spcname='space1';"""
        msg2 = self.commonsh.execut_db_sql(cmd2)
        log.info(msg2)
        self.assertTrue('10240 K' in msg2)
        log.info('------插入大小为736K的数据------')
        cmd3 = f"""insert into tb1 values(generate_series(1,20000));"""
        msg3 = self.commonsh.execut_db_sql(cmd3)
        log.info(msg3)
        self.assertTrue('INSERT 0 20000' in msg3)

        log.info('------测试点4:修改表空间size小于实际大小，修改成功------')
        log.info('------修改表空间space1的size为1K------')
        cmd4 = f"""alter tablespace space1 resize maxsize '1K';"""
        msg4 = self.commonsh.execut_db_sql(cmd4)
        log.info(msg4)
        self.assertTrue('ALTER TABLESPACE' in msg4)
        log.info('------再次插入数据，插入失败------')
        cmd5 = f"""insert into tb1 values(generate_series(1,20000));"""
        msg5 = self.commonsh.execut_db_sql(cmd5)
        log.info(msg5)
        self.assertTrue(error_info in msg5)

    def tearDown(self):
        msg = self.commonsh.execut_db_sql(self.drop)
        log.info(msg)
        log.info("--Opengauss_Function_DDL_Tablespace_Case0012结束--")
