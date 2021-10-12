--  @testpoint:修改OPTIONS中的字段,删除（drop）字段,待删除字段不存在，合理报错
--创建数据源对象
drop DATA SOURCE if exists ds_test9;
CREATE DATA SOURCE ds_test9 TYPE 'unknown' VERSION '11.2.3' OPTIONS (dsn 'openGauss',encoding 'utf-8');
--删除字段username，添加drop,合理报错
ALTER DATA SOURCE ds_test9 OPTIONS (drop username);
--删除数据源对象
DROP DATA SOURCE ds_test9;