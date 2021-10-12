-- @testpoint: cos函数与其它函数嵌套使用
select acos(cos(1)) from sys_dummy;
select cos(acos(1)) from sys_dummy;
select cos(acos(cos(acos(cos(acos(cos(acos(cos(acos(1)))))))))) from sys_dummy;