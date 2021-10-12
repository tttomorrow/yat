-- @testpoint: 函数嵌套使用

select sin(null) from sys_dummy;
select sin(sin(1)) from sys_dummy;
select cos(sin(1)) from sys_dummy;
select asin(sin(1)) from sys_dummy;
select sin(asin(1)) from sys_dummy;
select sin(asin(sin(asin(sin(asin(sin(asin(sin(asin(1)))))))))) from sys_dummy;