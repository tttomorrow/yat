--  @testpoint:修改OPTIONS中的字段,删除（drop）字段(多个字段)
--创建数据源对象
drop DATA SOURCE if exists ds_test9;
CREATE DATA SOURCE ds_test9 TYPE 'unknown' VERSION '11.2.3' OPTIONS (dsn 'openGauss',encoding 'utf-8');
--删除字段dsn，encoding,添加drop
ALTER DATA SOURCE ds_test9 OPTIONS (drop dsn,drop encoding);
select srcname,srctype,srcversion,srcacl,srcoptions from PG_EXTENSION_DATA_SOURCE where srcname = 'ds_test9';
--删除数据源对象
DROP DATA SOURCE ds_test9;





