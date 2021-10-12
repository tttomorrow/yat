--  @testpoint:修改数据源对象的type参数值
DROP DATA SOURCE if exists ds_test9;
CREATE DATA SOURCE ds_test9 TYPE 'unknown';
--修改type为空串
ALTER DATA SOURCE ds_test9 TYPE '';
select srcname,srctype,srcversion,srcacl,srcoptions from PG_EXTENSION_DATA_SOURCE where srcname = 'ds_test9';
--修改type为其他值
ALTER DATA SOURCE ds_test9 TYPE 'MPPDB';
select srcname,srctype,srcversion,srcacl,srcoptions from PG_EXTENSION_DATA_SOURCE where srcname = 'ds_test9';
--删除数据源对象
DROP DATA SOURCE ds_test9;