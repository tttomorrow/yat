--  @testpoint:修改OPTIONS中的字段,删除（drop）字段，指定optvalue，合理报错
--创建数据源对象
drop DATA SOURCE if exists ds_test9;
CREATE DATA SOURCE ds_test9 TYPE 'unknown' VERSION '11.2.3' OPTIONS (dsn 'openGauss',encoding 'utf-8');
--删除字段encoding，添加drop,合理报错
ALTER DATA SOURCE ds_test9 OPTIONS (drop encoding 'utf-8');
--删除数据源对象
DROP DATA SOURCE ds_test9;