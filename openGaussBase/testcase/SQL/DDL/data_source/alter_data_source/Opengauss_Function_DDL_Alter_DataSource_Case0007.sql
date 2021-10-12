--  @testpoint:修改OPTIONS中的字段,修改（SET）字段
--创建数据源对象
drop DATA SOURCE if exists ds_test9;
CREATE DATA SOURCE ds_test9 TYPE 'unknown' VERSION '11.2.3' OPTIONS (dsn 'openGauss',encoding 'utf_8');
--修改OPTIONS中的字段，添加set，修改dsn，其他值不变
ALTER DATA SOURCE ds_test9 OPTIONS (set dsn 'unknown');
select srcname,srctype,srcversion,srcacl,srcoptions from PG_EXTENSION_DATA_SOURCE where srcname = 'ds_test9';
--修改OPTIONS中的字段，省略set，修改encoding，其他值不变，合理报错
ALTER DATA SOURCE ds_test9 OPTIONS (encoding 'unknown');
--修改OPTIONS中的字段，添加set，修改username，其他值不变,合理报错
ALTER DATA SOURCE ds_test9 OPTIONS (set username 'test_user');
--删除数据源对象
DROP DATA SOURCE ds_test9;