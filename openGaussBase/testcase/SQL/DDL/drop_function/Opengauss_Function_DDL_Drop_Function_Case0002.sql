--  @testpoint:删除存在的函数添加IF EXISTS 子句并且添加函数参数，执行删除操作
drop FUNCTION if EXISTS u_testfun66(c_int int);
CREATE FUNCTION u_testfun66 ( INOUT c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/
select proname from pg_proc where proname='u_testfun66';
--添加IF EXISTS 子句并且添加函数参数，删除已存在的函数
drop FUNCTION if EXISTS u_testfun66(c_int int);