-- @testpoint: 不声明直接在包体中定义函数,合理报错

--step1:定义包体 expect:合理报错
create  or replace package body p_test_0019 is
function f_package_0019(c_int integer) returns integer as $$
begin
     return c_int  + 1;
end;
$$ language plpgsql;
end p_test_0019;
/