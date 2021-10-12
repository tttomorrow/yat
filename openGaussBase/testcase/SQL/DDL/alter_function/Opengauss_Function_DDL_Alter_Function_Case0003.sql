--  @testpoint:修改不存在的函数名，合理报错
select proname from pg_proc where proname='u_testfun55';
ALTER FUNCTION u_testfun55(c_int int)rename to u_testfun57;