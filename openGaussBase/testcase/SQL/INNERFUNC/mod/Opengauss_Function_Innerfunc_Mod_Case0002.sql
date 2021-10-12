-- @testpoint: mod函数入参超过固定个数，合理报错
select mod(154414,56598,44) from sys_dummy;
select mod(154414,0,44) from sys_dummy;
select mod(154414,null44) from sys_dummy;
select mod(154414,null,44) from sys_dummy;
select mod(154414,,44) from sys_dummy;
select mod(0,0,0) from sys_dummy;