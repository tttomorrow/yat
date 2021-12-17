-- @testpoint: mod函数有效值测试，分母为0时合理报错
select mod(154414,56598) from sys_dummy;
select mod(154414,5659.8) from sys_dummy;
select mod(154414,56592323238) from sys_dummy;
select mod(0,56592323238) from sys_dummy;
select mod(154414,'563238') from sys_dummy;
select mod('154414','56592323238') from sys_dummy;
select mod(1544324243242343423554543534414,56592323238434234234234234234234) from sys_dummy;
select mod(0444444454,01223) from sys_dummy;
select mod(0.444444454,0.1223) from sys_dummy;
select mod(0444444454,0.1223) from sys_dummy;
select mod(0000000,0.45410000000000) from sys_dummy;
select mod(-34234343534,32) from sys_dummy;
select mod(-34234343534,-32) from sys_dummy;