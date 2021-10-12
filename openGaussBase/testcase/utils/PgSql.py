"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

openGauss is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:

          http://license.coscl.org.cn/MulanPSL2

THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""

'''
    sql module
    使用python连接java程序，java去连接数据库
    （还可以使用gsql命令，-c 或者 -f 参数携带sql语句）

'''
import socket
import json
from .Logger import Logger
from yat.test import Node
from .Logger import Logger
from yat.test import macro

logger = Logger()

class PgSql():

    def __init__(self, database, node='dbuser'):
        '''
        初始化数据库连接，调用： psql = PgSql(database, dbconfigname), database为要连接的数据库名称。 dbconfigname默认使用 dbuser(见conf/nodes.yml)        '''
        ## 数据库用户连接
        dbNode = Node(node=node)
        self.databaseConfig = {
            'user':  dbNode.db_user,
            'port': dbNode.db_port,
            'host': dbNode.db_host,
            'password': dbNode.db_password,
            'database': database
        }
        self.dbNode = dbNode
        self.initSocketConnection()
        logger.error(self.databaseConfig)
        self.createDatabase(database)

        ## 默认不开启事务, 需要开启事务掉用setTransaction
        self.startTransaction = 'false'

    
    def createDatabase(self, database):
        '''
        创建数据库，使用gsql命令中 -c 参数携带sql语句
        '''
        createshell = '''
        source /home/{sshDbUser}/gaussdb.bashrc;
        gsql -d postgres -p {port} -r -c "create database {database};"
        '''.format(sshDbUser=self.dbNode.ssh_user, port=self.dbNode.db_port,database=database)
        msg = self.dbNode.sh(createshell).result()
        logger.info('create database ' + database)
        return msg

    
    def dropDatabase(self, database):
        '''
        删除数据库
        '''
        dropshell = '''
        source /home/{sshDbUser}/gaussdb.bashrc;
        gsql -d postgres -p {port} -r -c "drop database if exists {database};"
        '''.format(sshDbUser=self.dbNode.ssh_user, port=self.dbNode.db_port,database=database)
        msg = self.dbNode.sh(dropshell).result()
        logger.info('drop database ' + database)
        return msg


    def executerQuery(self, sql):
        '''
        适用于查询语句，有返回结果。
        返回结果为二维数据
        '''
        logger.info(sql)
        return self.connectAndSend(sql, 'query')


    def executerInsert(self, sql):
        '''
        表格插入数据
        '''
        logger.info(sql)
        return self.connectAndSend(sql, 'insert')


    def executerUpdate(self, sql):
        '''
        修改
        '''
        logger.info(sql)
        return self.connectAndSend(sql, 'update')


    def executerDelete(self, sql):
        '''
        删除
        '''
        logger.info(sql)
        return self.connectAndSend(sql, 'delete')


    def executer(self, sql):
        '''
        适用于建表、删表等语句
        '''
        logger.info(sql)
        return self.connectAndSend(sql)


    ## 设置是否开启事务提交
    def setTransaction(self, started):
        if started:
            self.startTransaction = 'true'
        else:
            self.startTransaction = 'false'


    def close(self):
        '''
        关闭数据库连接
        '''
        # self.connection.close()

    def initSocketConnection(self):
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #声明socket类型，同时生成链接对象
        client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        client.connect(('127.0.0.1',8080))
        self.client = client


    def connectAndSend(self, sql, type=''):

        ## send data
        configData = {
            'sql': sql,
            'config': self.databaseConfig,
            'type': type, ### query insert update delete,
            'transaction': self.startTransaction
        }
        sendData = str(configData)
        self.client.send( sendData.encode('utf-8'))

        if type == 'query':
            buffer = []
            while True:
                recvdata = self.client.recv(1024)  ##1024表示每次最多接收1024Byte:
                logger.info("in receiving data: " + str(len(recvdata)))
                if not recvdata or len(recvdata) == 0:
                    logger.info("receive empty break")
                    break
                else:
                    buffer.append(recvdata)
                    logger.info("receive length break:" + str(len(recvdata)))
                    if (len(recvdata) < 1024):
                        break
            logger.info("end receive data: " + str(len(buffer)))

            data = b''.join(buffer)
            result = str(data, encoding='utf-8')
            return json.loads(result)
        else:
            buffer = []
            d = self.client.recv(1024)
            buffer.append(d)
            data = b''.join(buffer)
            return str(data, encoding='utf-8')
