--  @testpoint:创建数据源对象,添加type选项
--创建数据源对象,type非空
DROP DATA SOURCE if exists ds_test4;
CREATE DATA SOURCE ds_test4 type 'MPPDB';
--查询创建的数据源对象信息
select srcname,srctype,srcversion,srcacl,srcoptions from PG_EXTENSION_DATA_SOURCE where srcname = 'ds_test4';
--删除数据源对象
DROP DATA SOURCE ds_test4;