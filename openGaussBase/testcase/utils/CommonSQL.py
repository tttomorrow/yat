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

数据库执行公共SQL

"""
from testcase.utils.CommonSH import CommonSH


class CommonSQL(CommonSH):
    def __init__(self, node_name='dbuser'):
        """
        初始化
        :param node_name: 通过root用户还是数据库安装的用户执行脚本（见 conf/nodes.yml）
        """
        CommonSH.__init__(self, node_name)

    def create_func(self, func_name='', var='', execute_sql='', start='',
                    end='', step=''):
        """
        创建公用function，按照间隔值执行特定SQL
        return: func_name
        """
        function_cmd = f'''create or replace function {func_name}(num int)
            returns void as \$\$
            declare 
                {var} int;
            begin
                if num < {start} then 
                    for {var} in 0..num loop 
                        {execute_sql}
                    end loop;
                elsif num >= {start} and num < {start}+{step}*1 then
                    for {var} in {start}..num loop 
                        {execute_sql}
                    end loop;
                elsif num >= {start}+{step}*1 and num < {start}+{step}*2 then
                    for {var} in {start}+{step}*1..num loop 
                        {execute_sql}
                    end loop;
                elsif num >= {start}+{step}*2 and num < {end} then
                    for {var} in {start}+{step}*2..num loop 
                        {execute_sql}
                    end loop;
                end if;
            end;
            \$\$ language plpgsql;'''
        self.log.info(function_cmd)
        function_msg = self.execut_db_sql(function_cmd)
        self.log.info(function_msg)
        if function_msg.find(self.Constant.CREATE_FUNCTION_SUCCESS_MSG) > -1:
            return func_name
        else:
            self.log.info('---创建函数失败---')
            return False

