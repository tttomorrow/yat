-- @testpoint: 输入参数为可转成数值型的表达式

select sin('') from sys_dummy;
select sin('' + 1) from sys_dummy;
select sin('' * 1) from sys_dummy;
select sin(''||1) from sys_dummy;
select sin(1) from sys_dummy;
select sin(''||1)+sin(-1) from sys_dummy;
select sin(-1) from sys_dummy;