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
Case Type   : Trigger
Case Name   : MOT不支持触发器
Description :
    1、修改enable_incremental_checkpoint=off
    2、重启数据库,gs_om -t stop && gs_om -t start
    3、创建内存表外表&源表，创建触发器函数，创建触发器；
    4、清理数据;
Expect      :
    1、修改成功；
    2、重启数据库成功；
    3、创建表成功，创建触发器函数成功，创建触发器失败；
    4、清理环境成功；
History     :
"""
import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common

LOG = Logger()
CONSTANT = Constant()
Primary_SH = CommonSH('PrimaryDbUser')


class TriggerMotTest(unittest.TestCase):
    def setUp(self):
        LOG.info("======Opengauss_Function_Trigger_Case0055开始执行======")
        self.common = Common()

    def test_trigger_mot(self):
        LOG.info("======检查参数，修改配置，并重启数据库======")
        self.config_item = 'enable_incremental_checkpoint=off'
        sql_cmd0 = 'show enable_incremental_checkpoint;'
        check_res = Primary_SH.execut_db_sql(sql_cmd0)
        LOG.info(check_res)
        if check_res.splitlines()[2].strip() != 'off':
            Primary_SH.execute_gsguc('set', CONSTANT.GSGUC_SUCCESS_MSG,
                                     self.config_item, single=True)
            result = Primary_SH.restart_db_cluster()
            LOG.info(result)
            self.assertTrue(result)
        LOG.info("=======步骤1：创建内存表 外表&源表=======")
        sql_cmd1 = f'drop foreign table if exists test_src;' \
                   f'drop foreign table if exists test_dec;' \
                   f'create foreign table test_src(id1 int,id2 int,id3 int);' \
                   f'create foreign table test_dec(id1 int,id2 int,id3 int);'
        LOG.info(sql_cmd1)
        create_res1 = Primary_SH.execut_db_sql(sql_cmd1)
        LOG.info(create_res1)
        self.assertIn(CONSTANT.CREATE_FOREIGN_SUCCESS_MSG, create_res1)
        LOG.info("======步骤2：创建触发器函数 & 触发器======")
        create_cmd2 = '''
            create or replace function tri_insert() returns trigger
            as
            \$\$
            declare
            begin
            insert into test_dec values(NEW.id1,NEW.id2,NEW.id3);
            return NEW;
            end
            \$\$ language plpgsql;
            create trigger insert_trigger before insert on
            test_src for each row execute procedure tri_insert();
            '''
        LOG.info(create_cmd2)
        create_res2 = Primary_SH.execut_db_sql(create_cmd2)
        LOG.info(create_res2)
        self.assertIn('not a table or view', create_res2)

    def tearDown(self):
        LOG.info("======清理环境,恢复配置======")
        del_cmd = f'drop foreign table test_src;' \
                  f'drop foreign table test_dec;' \
                  f'drop function tri_insert();'
        LOG.info(del_cmd)
        del_msg = Primary_SH.execut_db_sql(del_cmd)
        LOG.info(del_msg)
        sql_cmd1 = 'show enable_incremental_checkpoint;'
        check_res = Primary_SH.execut_db_sql(sql_cmd1)
        LOG.info(check_res)
        if check_res.splitlines()[2].strip() == 'off':
            Primary_SH.execute_gsguc('set', CONSTANT.GSGUC_SUCCESS_MSG,
                                     'enable_incremental_checkpoint=on',
                                     single=True)
            result = Primary_SH.restart_db_cluster()
            LOG.info(result)
            self.assertTrue(result)
        LOG.info("======Opengauss_Function_Trigger_Case0055执行结束======")
