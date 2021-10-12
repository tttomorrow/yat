-- @testpoint: 函数嵌套使用测试


select asin(sin(1)) as result from sys_dummy;
select cast(asin(asin(0.5))as numeric(3,2)) as result from sys_dummy;
select cast(asin('0.6')as numeric(3,2)) as result from sys_dummy;