-- @testpoint: 声明package时定义函数,合理报错

--step1:声明package,定义函数 expect:合理报错
create or replace package p_test_0014 is
function f_package_0014(c_int integer) returns integer is
begin
     return c_int + 1;
end;
end p_test_0014;
/