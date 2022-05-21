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
Case Name   : 查看gs_probackup set-config命令的摘要信息
Description :
    1.执行命令显示gs_probackup set-config命令的摘要信息
Expect      :
    1.显示gs_probackup set-config命令的摘要信息成功
History     :
"""

import unittest
import os
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.except_msg = '''
        gs_probackup set-config 
        -B backup-path --instance=instance_name
        [-D pgdata-path] 
        [-E external-directories-paths]
        [--archive-timeout=timeout]
        [--retention-redundancy=retention-redundancy]
        [--retention-window=retention-window]
        [--wal-depth=wal-depth]
        [--compress-algorithm=compress-algorithm]
        [--compress-level=compress-level]
        [-d dbname] [-h host] [-p port] [-U username]
        [--log-level-console=log-level-console]
        [--log-level-file=log-level-file]
        [--log-filename=log-filename]
        [--error-log-filename=error-log-filename]
        [--log-directory=log-directory]
        [--log-rotation-size=log-rotation-size]
        [--log-rotation-age=log-rotation-age]
        [--remote-proto=protocol] [--remote-host=destination]
        [--remote-path=path] [--remote-user=username]
        [--remote-port=port] [--ssh-options=ssh_options]   
        [--remote-libpath=libpath]
        -B, --backup-path=backup-path    
        location of the backup storage area
        --instance=instance_name     name of the instance
        -D, --pgdata=pgdata-path         
        location of the database storage area
        -E, --external-dirs=external-directories-paths
        backup some directories not from pgdata
        (example: --external-dirs=/tmp/dir1:/tmp/dir2)
        --archive-timeout=timeout    
        wait timeout for WAL segment archiving (default: 5min)  
        Retention options:
        --retention-redundancy=retention-redundancy
        number of full backups to keep; 0 disables; (default: 0)
        --retention-window=retention-window
        number of days of recoverability; 0 disables; (default: 0)
        --wal-depth=wal-depth        
        number of latest valid backups with ability to perform
        the point in time recovery;  disables; (default: 0)
        Compression options:
        --compress-algorithm=compress-algorithm
        available options: 'zlib','pglz','none' (default: 'none')
        --compress-level=compress-level
        level of compression [0-9] (default: 1)
        Connection options:
        -U, --pguser=username            
        user name to connect as (default: current local user)
        -d, --pgdatabase=dbname          d
        atabase to connect (default: username)
        -h, --pghost=hostname            
        database server host or socket directory(default: 'local socket')
        -p, --pgport=port                
        database server port (default: 5432)
        Logging options:
        --log-level-console=log-level-console
        level for console logging (default: info)
        available options: 'off', 'error', 
        'warning', 'info', 'log', 'verbose'
        --log-level-file=log-level-file
        level for file logging (default: off)
        available options: 'off', 'error', 
        'warning', 'info', 'log', 'verbose'
        --log-filename=log-filename
        filename for file logging (default: 'pg_probackup.log')
        support strftime format 
        (example: pg_probackup-%Y-%m-%d_%H%M%S.log)
        --error-log-filename=error-log-filename
        filename for error logging (default: none)
        --log-directory=log-directory
        directory for file logging (default: BACKUP_PATH/log)
        --log-rotation-size=log-rotation-size
        rotate logfile if its size exceeds this value; 
        0 disables; (default: 0)
        available units: 'kB', 'MB', 'GB', 'TB' (default: kB)
        --log-rotation-age=log-rotation-age
        rotate logfile if its age exceeds this value; 0 disables; 
        (default: 0)
        available units: 'ms', 's', 'min', 'h', 'd' (default: min)
        Remote options:
        --remote-proto=protocol      remote protocol to use
        available options: 'ssh', 'none' (default: ssh)
        --remote-host=destination    remote host address or hostname
        --remote-port=port           remote host port (default: 22)
        --remote-path=path           
        path to directory with gs_probackup binary on remote host
        (default: current binary path)
        --remote-user=username       
        user name for ssh connection (default: current user)
        --remote-libpath=libpath         library path on remote host
        --ssh-options=ssh_options    
        additional ssh options (default: none)
        (example: --ssh-options='-c cipher_spec -F configfile')'''

    def test_system_internal_tools(self):
        self.log.info('step1 执行命令显示gs_probackup set-config命令的摘要信息')
        help_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup set-config --help;"
        self.log.info(help_cmd)
        help_msg = self.PrimaryNode.sh(help_cmd).result()
        self.log.info(help_msg)
        line_msg = help_msg.splitlines()
        self.log.info(line_msg)
        for line in line_msg:
            if line:
                for part in line.split():
                    self.assertIn(part.strip(), self.except_msg)

    def tearDown(self):
        # 无须清理环境
        self.log.info(f'-----{os.path.basename(__file__)} end-----')
