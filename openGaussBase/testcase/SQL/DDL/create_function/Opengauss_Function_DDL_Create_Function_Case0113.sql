--  @testpoint:创建函数，指定函数的执行模式是not fenced
drop FUNCTION if EXISTS u_testfun0(c_int int);
CREATE FUNCTION u_testfun0 (c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql
STRICT
not fenced ;
/

call u_testfun0(999);
drop FUNCTION u_testfun0;