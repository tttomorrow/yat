--  @testpoint:修改数据源对象的version参数值
drop DATA SOURCE if exists ds_test11;
CREATE DATA SOURCE ds_test11 TYPE 'unknown' VERSION '11.2.3';
select srcname,srctype,srcversion,srcacl,srcoptions from PG_EXTENSION_DATA_SOURCE where srcname = 'ds_test11';
--修改version值,其他参数值保持不变
ALTER DATA SOURCE ds_test11 version '1.0.0';
select srcname,srctype,srcversion,srcacl,srcoptions from PG_EXTENSION_DATA_SOURCE where srcname = 'ds_test11';
--修改version值为空串,其他参数值保持不变
ALTER DATA SOURCE ds_test11 version '';
select srcname,srctype,srcversion,srcacl,srcoptions from PG_EXTENSION_DATA_SOURCE where srcname = 'ds_test11';
--修改version值为null，其他参数值保持不变
ALTER DATA SOURCE ds_test11 version null;
--删除数据源对象
DROP DATA SOURCE ds_test11;