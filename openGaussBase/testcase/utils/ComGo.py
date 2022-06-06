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
"""go驱动相关公共类"""
import re


class ComGo:
    def __init__(self):
        pass

    @staticmethod
    def conndb(param_name):
        """返回go语言数据库连接信息语句"""
        res_str = f"var db *sql.DB\n" \
            f"    db, err := sql.Open(\"opengauss\", {param_name})\n" \
            f"    if err != nil {{\n" \
            f"        panic(err)\n" \
            f"    }}"

        return res_str

    @staticmethod
    def exec_sql(sql, first_flag=True):
        """返回go语言数据库执行语句"""
        res_str = f"res, err := db.Exec(\"{sql}\")\n" \
            f"    if err != nil {{\n" \
            f"        panic(err)\n" \
            f"    }}\n" \
            f"    fmt.Println(res)"

        if not first_flag:
            res_str = res_str.replace(':=', '=')

        return res_str

    @staticmethod
    def query_row(sql, **params):
        """
        :param sql: 数据查询语句
        :param params: 字典{查询参数:查询参数类型}
        :return: go语言数据库单行查询语句
        """
        define_str = ""
        sql_str = ""
        print_str = ""
        for param, type_param in params.items():
            define_str += f"var {param} {type_param}\n" + ' '*4
            sql_str += f"&{param},"
            print_str += f"{param},"
        res_str = define_str + '\n' + \
            f"    err = db.QueryRow(\"{sql}\").Scan({sql_str.strip(',')})\n" \
            + f"    if err != nil {{\n" + \
            f"        panic(err)\n" + \
            f"    }}\n" + \
            f"    fmt.Println({print_str.strip(',')})"

        return res_str

    @staticmethod
    def query(sql, first_flag=True, **params):
        """
        :param sql: 数据查询语句
        :param first_flag: 首次调用标志，首次调用为True，其他为False
        :param params: 字典{查询参数:查询参数类型}
        :return: go语言数据库多行查询语句
        """
        define_str = ""
        sql_str = ""
        print_str = ""
        for param, type_param in params.items():
            define_str += f"var {param} {type_param}\n" + ' '*4
            sql_str += f"&{param},"
            print_str += f"{param},"
        res_str = define_str + '\n' + \
            f"    rows, err := db.Query(\"{sql}\")\n" + \
            f"    for rows.Next() {{\n" + \
            f"        err := rows.Scan({sql_str.strip(',')})\n" + \
            f"        if err != nil {{\n" + \
            f"            panic(err)\n" + \
            f"        }}\n" + \
            f"        fmt.Println({print_str.strip(',')})\n" + \
            f'  }}'

        if not first_flag:
            res_str = res_str.replace(':=', '=')

        return res_str

    @staticmethod
    def check_install_go(node, version):
        """前置校验：node环境已安装golang version以上版本"""
        try:
            if 'CentOS' in node.sh('cat /etc/system-release').result():
                cmd = 'source /etc/profile && go version'
            else:
                cmd = 'go version'
            res = node.sh(cmd).result()
            assert 'go: command not found' not in res
            cur_version = re.search(r'go\d+.\d+.\d+', res).group().strip('go')
            assert cur_version >= version
        except Exception as e:
            print(str(e))
            return False
        else:
            return True

    @staticmethod
    def get_head():
        str_res = 'package main\n' \
                  'import (\n' \
                  '    "database/sql"\n' \
                  '    "fmt"\n' \
                  '    _ "gitee.com/opengauss/openGauss-connector-go-pq"\n' \
                  ')'

        return str_res
