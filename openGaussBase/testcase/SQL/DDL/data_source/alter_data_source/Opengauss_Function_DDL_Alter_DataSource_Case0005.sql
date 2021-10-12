--  @testpoint:修改OPTIONS中的字段,增加（ADD）字段
--创建数据源对象
DROP DATA SOURCE if exists ds_test13;
create DATA SOURCE ds_test13;
--添加字段，使用add，待增加字段不存在
ALTER DATA SOURCE ds_test13 OPTIONS (add dsn 'opengauss');
select srcname,srctype,srcversion,srcacl,srcoptions from PG_EXTENSION_DATA_SOURCE where srcname = 'ds_test13';
--添加字段，省略add，待增加字段不存在
ALTER DATA SOURCE ds_test13 OPTIONS (encoding 'UTF-8');
select srcname,srctype,srcversion,srcacl,srcoptions from PG_EXTENSION_DATA_SOURCE where srcname = 'ds_test13';
--删除数据源对象
DROP DATA SOURCE ds_test13;