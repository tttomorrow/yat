#!/usr/bin/env python
# encoding=utf-8
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


class DataGenerator:
    BATCH_COUNT = 500

    def __init__(self, db, table_name, count, **column_metas):
        self.db = db
        self.table_name = table_name
        self.count = count
        self.column_metas = column_metas

    def _make_sql_template(self):
        return 'insert into {table_name} ({columns}) values ({values})'.format(
            table_name=self.table_name,
            columns=','.join(self.column_metas.keys()),
            values=','.join('?'*len(self.column_metas)))

    def generate(self):
        sql = self._make_sql_template()
        cache = []
        for i in range(self.count):
            cache.append(self._gen_line())
            if i % self.BATCH_COUNT == 0:
                self.db.execute(sql, *cache)
                cache = []

        if len(cache) > 0:
            self.db.execute_query(sql, *cache)

    def _gen_line(self):
        res = []
        for name in self.column_metas:
            meta = self.column_metas[name]
            res.append(self._gen_element(meta))
        return res

    def _gen_element(self, meta):
        if 'value' in meta:
            return meta['value']

        tp = meta['type']
        if tp == 'str':
            pass


