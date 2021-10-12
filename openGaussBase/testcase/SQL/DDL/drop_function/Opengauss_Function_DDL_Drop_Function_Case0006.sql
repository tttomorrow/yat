--  @testpoint:删除存在的函数省略IF EXISTS 子句并且添加函数参数，执行删除操作
drop FUNCTION if EXISTS u_testfun79(c_int int);
CREATE FUNCTION u_testfun79 ( INOUT c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/
select proname from pg_proc where proname='u_testfun79';
--省略IF EXISTS子句并且添加函数参数，删除成功
drop FUNCTION  u_testfun79(c_int int);