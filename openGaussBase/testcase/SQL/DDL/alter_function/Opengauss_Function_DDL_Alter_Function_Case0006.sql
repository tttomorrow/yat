--  @testpoint:修改函数名时带原有函数的参数模式、参数名、参数类型、合理报错
--创建函数名为u_testfun50的函数
drop FUNCTION if EXISTS u_testfun50(c_int int);
CREATE FUNCTION u_testfun50 (INOUT c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql
STRICT;
/
select proargnames,proname from pg_proc where proname='u_testfun50';
--修改函数名u_testfun50为 u_testfun60
ALTER FUNCTION u_testfun50(c_int int) rename to u_testfun60(INOUT c_int int);
drop FUNCTION u_testfun50;