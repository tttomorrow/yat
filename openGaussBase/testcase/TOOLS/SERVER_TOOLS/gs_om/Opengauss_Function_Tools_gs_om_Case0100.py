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
Case Type   : 服务端工具
Case Name   : 级联备主备切换--switchover将级联备升成备机后,再次switchover将备机升成主机,查询数据库状态及节点信息
Description :
    1.将备1切换为级联备后再将级联备切换备机
    2.将备机切换为主机
    3.结合--detail参数,查看数据库状态及节点详细信息
      校验是否有port字段,校验备机IP是否发生变化，校验备机port端口号
        gs_om -t status --detail
    4.结合--all参数，查看数据库状态及所有节点信息
      校验是否有port字段，校验备机IP是否发生变化，校验备机port端口号
        gs_om -t status --all
    5.结合-h,-o参数，查看指定数据库节点状态及信息(-h指定切换后的备机/级联备)
      校验是否有输出文件及日志，输出文件及日志中是否有port字段
      校验备机IP是否发生变化，校验备机port端口号
        gs_om -t status -h hostname -o status.txt
    6.query查询数据状态及相关信息
      校验备机IP是否发生变化，校验备机port端口号
        gs_om -t query -o status.txt
    7.恢复原有集群状态
    8.清理环境，删除文件信息
Expect      :
    1.备机切换为级联备成功
    2.备机切换为主机成功
    3.显示状态详细信息，原有主备状态发生改变,存在port字段,且端口号正确
    4.显示数据库所有节点信息,原有主备状态发生改变,存在port字段,且端口号正确
    5.显示指定节点状态信息,指定节点为原主机(换后的备机),且端口号正确
    6.显示数据库状态信息,原有主备状态发生改变，存在port字段,且端口号正确
    7.恢复集群原有状态成功
    8.清理环境成功
History     : 
"""
import os
import time
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(3 != Primary_SH.get_node_num(), '非1+2环境不执行')
class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        text = f'-----{os.path.basename(__file__)} start-----'
        self.log.info(text)
        self.pri_node = Node("PrimaryDbUser")
        self.nodelist = ['Standby1DbUser', 'Standby2DbUser']
        self.node_num = Primary_SH.get_node_num()
        result = Primary_SH.get_db_cluster_status('detail')
        self.log.info(result)
        self.node_num = result.count('Standby Normal') + 1
        self.log.info(self.node_num)
        self.comshsta = []
        self.common = Common()
        self.constant = Constant()
        self.output_path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'output.txt')

    def test_tools_om(self):
        if self.node_num > 2:
            for i in range(int(self.node_num) - 1):
                self.comshsta.append(CommonSH(self.nodelist[i]))
            text = '-----step1.1:将备1 build为级联备;except:备机切换为级联备成功-----'
            self.log.info(text)
            result = self.comshsta[0].build_standby('-M cascade_standby')
            self.assertIn(self.constant.REBUILD_SUCCESS_MSG, result,
                          '执行失败' + text)
            result = self.comshsta[0].exec_refresh_conf()
            self.assertTrue(result, '执行失败' + text)

            self.log.info('--------等待主备一致------------')
            result = self.comshsta[1].check_data_consistency()
            self.assertTrue(result, '执行失败' + text)
            for i in range(90):
                result = Primary_SH.check_cascade_standby_consistency()
                if result:
                    break
                time.sleep(20)
            self.assertTrue(result, '执行失败' + text)
            status = Primary_SH.get_db_cluster_status("detail")
            self.log.info(status)

            text = '-----step1.2:将级联备切换为备机;except:级联备备机切换成功-----'
            self.log.info(text)
            result = self.comshsta[0].execute_gsctl(
                'switchover', self.constant.SWITCHOVER_SUCCESS_MSG,
                '-M standby')
            self.assertTrue(result, '执行失败' + text)
            result = self.comshsta[0].exec_refresh_conf()
            self.assertTrue(result, '执行失败' + text)
            self.log.info('--------等待主备一致------------')
            result = self.comshsta[0].check_data_consistency()
            self.assertTrue(result, '执行失败' + text)
            for i in range(90):
                result = Primary_SH.check_cascade_standby_consistency()
                if result:
                    break
                time.sleep(20)
            self.assertTrue(result, '执行失败' + text)
            status = Primary_SH.get_db_cluster_status("detail")
            self.log.info(status)

            text = '-----step2:将备机切换为主机;except:主备机切换成功-----'
            self.log.info(text)
            result = self.comshsta[0].execute_gsctl(
                'switchover', self.constant.SWITCHOVER_SUCCESS_MSG)
            self.assertTrue(result, '执行失败' + text)
            result = self.comshsta[0].exec_refresh_conf()
            self.assertTrue(result, '执行失败' + text)
            self.log.info('--------等待主备一致------------')
            result = self.comshsta[0].check_data_consistency()
            self.assertTrue(result)
            for i in range(90):
                result = Primary_SH.check_cascade_standby_consistency()
                if result:
                    break
                time.sleep(20)
            self.assertTrue(result, '执行失败' + text)
            status = Primary_SH.get_db_cluster_status("detail")
            self.log.info(status)

            text = '-----step3:结合--detail参数，查看数据库状态及节点详细信息;' \
                   'except:显示状态详细信息，原有主备状态发生改变,存在port字段,' \
                   '且端口号正确-----'
            self.log.info(text)
            self.log.info('----------------获取端口信息-----------------')
            sql_cmd = f'''show port;'''
            show_port_res = Primary_SH.execut_db_sql(sql_cmd)
            node_port = show_port_res.splitlines()[-2].strip()
            self.log.info(node_port)
            status = Primary_SH.get_db_cluster_status("detail")
            self.log.info(status)
            self.assertIn('port', status.splitlines()[8], '执行失败' + text)

            text = '-----step4:结合--all参数，查看数据库状态及节点信息;' \
                   'expect:显示数据库所有节点信息,原有主备状态发生改变,' \
                   '存在port字段,且端口号正确----'
            self.log.info(text)
            new_status_list = []
            new_port_list = []
            shell_res = Primary_SH.get_db_cluster_status(param='all')
            self.log.info(shell_res)
            res = shell_res.splitlines()
            for param in res:
                if 'instance_role' in param:
                    new_status_list.append(param)
                if 'instance_port' in param:
                    new_port_list.append(param)
            self.log.info(new_status_list)
            self.log.info(new_port_list)
            self.log.info("======主机停止成功 && port正确======")
            try:
                if 'Down' in new_status_list[0]:
                    self.log.info("======主节点停止成功======")
            except Exception as e:
                self.log.info("======主节点未停止成功======")
                raise e
            finally:
                self.log.info("======主机状态校验完成======")
            try:
                if node_port == new_port_list[0].split(':')[1].strip():
                    self.log.info("======端口信息一致======")
            except Exception as e:
                self.log.info("======端口信息不一致======")
                raise e
            finally:
                self.log.info("======端口校验完成======")

            text = '-------step5:结合-h,-o参数，查看指定数据库节点状态及信息(-h指定切换后的备机);' \
                   'except:显示指定节点状态信息,指定节点为原主机(换后的备机),且端口号正确-------'
            self.log.info(text)
            shell_name = f'''hostname'''
            hostname = self.pri_node.sh(shell_name).result()
            self.log.info(hostname)
            shell_res = Primary_SH.get_db_cluster_status(
                param='other',
                args=f'status -h {hostname} '
                f'-o {self.output_path}')
            self.log.info(shell_res)
            shell_res = Primary_SH.get_db_cluster_status(
                param='other',
                args=f'status -h {hostname} -o {self.output_path}')
            self.log.info(shell_res)
            self.log.info("======当前节点port正确======")
            port_res = self.pri_node.sh(
                f'''cat {self.output_path} | grep instance_port''').result()
            self.log.info(port_res)
            self.assertIn(node_port, port_res, '执行失败' + text)

            text = '-----step6:query查询数据状态及相关信息;except:显示数据库状态信息,' \
                   '原有主备状态发生改变，存在port字段,且端口号正确-------'
            self.log.info(text)
            shell_res = Primary_SH.get_db_cluster_status(param='other',
                                                         args='query')
            self.log.info(shell_res)
            self.assertEqual('port',
                             shell_res.splitlines()[8].split()[2].strip(),
                             '执行失败' + text)

    def tearDown(self):
        text = '------step7:恢复原有集群状态;except:恢复集群原有状态成功----'
        self.log.info(text)
        if self.node_num > 2:
            result = Primary_SH.execute_gsctl(
                'switchover', self.constant.SWITCHOVER_SUCCESS_MSG)
            self.log.info(result)
            result = Primary_SH.exec_refresh_conf()
            self.log.info(result)
            for i in range(int(self.node_num) - 1):
                self.comshsta[i].build_standby('-M standby')
                result = self.comshsta[i].exec_refresh_conf()
                self.log.info(result)
        self.log.info('-----------重启数据库-----------')
        result = Primary_SH.execute_gsctl("restart",
                                          self.constant.REBUILD_SUCCESS_MSG)
        self.log.info(result)
        db_status = Primary_SH.get_db_cluster_status("detail")

        text = '------step8:清理环境;expect:清理环境成功------'
        self.log.info(text)
        clear_cmd = f'rm -rf {self.output_path};'
        self.log.info(clear_cmd)
        clear_msg = self.pri_node.sh(clear_cmd).result()
        self.log.info(clear_msg)
        self.assertEqual('', clear_msg, '执行失败' + text)
        self.assertTrue("Normal" in db_status or "Degraded" in db_status,
                        '执行失败' + text)
        text = f'-----{os.path.basename(__file__)} end-----'
        self.log.info(text)
