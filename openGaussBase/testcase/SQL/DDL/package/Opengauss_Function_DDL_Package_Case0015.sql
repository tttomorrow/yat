-- @testpoint: package名称中含空格,合理报错

--step1:声明package,名称含空格 expect:合理报错
create or replace package p test_0015 is
function f_package_0015(c_int int) return integer ;
end p_test_0015;
/