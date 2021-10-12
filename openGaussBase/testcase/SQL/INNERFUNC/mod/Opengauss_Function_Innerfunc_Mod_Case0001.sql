-- @testpoint: mod函数有效值测试，分母为0时合理报错
select mod(154414,56598) from sys_dummy;
select mod(154414,5659.8) from sys_dummy;
select mod(154414,'563238') from sys_dummy;
