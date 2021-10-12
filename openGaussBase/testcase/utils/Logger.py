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
    log module

'''

import logging


LOG_CONF = {
    'filename': './root.log',
    'level': 'INFO',
    'format': '[%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d] %(message)s',
    'datefmt': "%Y-%m-%d %H:%M:%S"
}

logging.basicConfig(**LOG_CONF)

class Logger:
    
    def debug(self, msg, *args):
        logging.debug(msg, *args)

    def info(self, msg, *args):
        logging.info(msg, *args)

    def warn(self, msg, *args):
        logging.warn(msg, *args)

    def error(self, msg, *args):
        logging.error(msg, *args)
