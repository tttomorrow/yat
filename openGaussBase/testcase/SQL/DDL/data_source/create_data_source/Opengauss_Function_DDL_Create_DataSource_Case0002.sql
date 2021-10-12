--  @testpoint:创建数据源对象，Data Source名称在数据库中不唯一
--查询系统表PG_EXTENSION_DATA_SOURCE，检查是否存在Data Source名称为ds_test2(不存在)
DROP DATA SOURCE if exists ds_test2;
select srcname from PG_EXTENSION_DATA_SOURCE where srcname = 'ds_test2';
--创建数据源对象，不含任何信息
CREATE DATA SOURCE ds_test2;
--查询创建的数据源对象信息
select srcname,srctype,srcversion,srcacl,srcoptions from PG_EXTENSION_DATA_SOURCE where srcname = 'ds_test2';
--再次创建DATA SOURCE，名称为已存在的ds_test2，合理报错
CREATE DATA SOURCE ds_test2;
--删除创建的数据源对象
DROP DATA SOURCE ds_test2;