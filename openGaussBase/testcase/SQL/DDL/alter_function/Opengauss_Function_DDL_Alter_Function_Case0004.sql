--  @testpoint:修改函数名，函数名不符合标识符命名规范
--创建函数名为u_testfun50的函数
drop FUNCTION if EXISTS u_testfun50(c_int int);
CREATE FUNCTION u_testfun50 (c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql
STRICT;
/
select proargnames,proname from pg_proc where proname='u_testfun50';

--修改函数名u_testfun50为 1_testfun60，合理报错
ALTER FUNCTION u_testfun50(c_int int)rename to 1_testfun60;
drop FUNCTION u_testfun50;