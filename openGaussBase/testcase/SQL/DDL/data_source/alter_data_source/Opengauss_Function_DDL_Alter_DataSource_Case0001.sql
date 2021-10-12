--  @testpoint:修改数据源对象名字
--创建数据源对象
DROP DATA SOURCE if exists ds_test13;
create DATA SOURCE ds_test13;
--修改数据源对象名字(原数据源名字已存在)
ALTER DATA SOURCE ds_test13 rename to new_ds_test13;
--修改数据源对象名字(原数据源名字不存在)，合理报错
DROP DATA SOURCE if exists test_ds_test12;
select srcname from PG_EXTENSION_DATA_SOURCE where srcname = 'test_ds_test12';
ALTER DATA SOURCE test_ds_test12 rename to test_ds_test13;
--删除数据源对象
DROP DATA SOURCE new_ds_test13;