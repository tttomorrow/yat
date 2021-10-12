--  @testpoint:修改函数名称为新的函数名，然后再修改回原来的函数名
--创建函数名为u_testfun5的函数
drop FUNCTION if EXISTS u_testfun5(c_int int);
CREATE FUNCTION u_testfun5 (c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql
STRICT;
/
select proargnames,proname from pg_proc where proname='u_testfun5';

--修改函数名u_testfun5为 u_testfun6
ALTER FUNCTION u_testfun5(c_int int)rename to u_testfun6;
select proargnames,proname from pg_proc where proname='u_testfun6';
--修改函数名u_testfun6为 u_testfun5
ALTER FUNCTION u_testfun6(c_int int)rename to u_testfun5;
select proargnames,proname from pg_proc where proname='u_testfun5';
drop FUNCTION u_testfun5;