--  @testpoint:创建数据源对象,添加version选项
--version为空串
DROP DATA SOURCE if exists ds_test5;
CREATE DATA SOURCE ds_test5 type 'MPPDB' version '';
--查询创建的数据源对象信息
select srcname,srctype,srcversion,srcacl,srcoptions from PG_EXTENSION_DATA_SOURCE where srcname = 'ds_test5';
--version为null
DROP DATA SOURCE if exists ds_test6;
CREATE DATA SOURCE ds_test6 type 'MPPDB' version null;
--查询创建的数据源对象信息
select srcname,srctype,srcversion,srcacl,srcoptions from PG_EXTENSION_DATA_SOURCE where srcname = 'ds_test6';
--version为非空
DROP DATA SOURCE if exists ds_test7;
CREATE DATA SOURCE ds_test7 type 'MPPDB' version '1.0.0';
--查询创建的数据源对象信息
select srcname,srctype,srcversion,srcacl,srcoptions from PG_EXTENSION_DATA_SOURCE where srcname = 'ds_test7';
--删除数据源对象
DROP DATA SOURCE ds_test5;
DROP DATA SOURCE ds_test6;
DROP DATA SOURCE ds_test7;