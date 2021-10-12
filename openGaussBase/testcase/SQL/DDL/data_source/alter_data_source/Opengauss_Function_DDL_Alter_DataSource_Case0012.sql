--  @testpoint:修改数据源对象的属主为普通用户，合理报错
drop DATA SOURCE if exists ds_test9;
CREATE DATA SOURCE ds_test9 TYPE 'unknown' VERSION '11.2.3' OPTIONS (dsn 'openGauss',encoding 'utf-8');
--创建普通用户
drop user if exists test_pt cascade;
create user test_pt password 'Xiaxia@123';
--修改属主为test_pt，合理报错
ALTER DATA SOURCE ds_test9 OWNER TO test_pt;
--删除数据源对象
DROP DATA SOURCE ds_test9;
--删除用户
drop user test_pt cascade;