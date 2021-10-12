-- @testpoint: lengthb函数特殊字符
select lengthb('######&^$*&%*&%#^%^') from sys_dummy;

select lengthb(-0.336) from sys_dummy;

select lengthb(3.354009) from sys_dummy;