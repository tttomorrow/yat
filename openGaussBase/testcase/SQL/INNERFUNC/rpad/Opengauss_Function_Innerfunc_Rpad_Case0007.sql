-- @testpoint: rpad函数异常测试，合理报错
select rpad('dss','gogogo','111') from sys_dummy;
select rpad(ARRAY[1,2,3],'30','111') from sys_dummy;
select rpad('dss',13,raw) from sys_dummy;
select rpad(13) from sys_dummy;