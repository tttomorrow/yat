--  @testpoint:删除已存在的函数添加IF EXISTS 子句并且添加函数参数，执行删除操作后再次执行删除语句,前后执行结果提示不一样
drop FUNCTION if EXISTS u_testfun68(c_int int);
CREATE FUNCTION u_testfun68 ( INOUT c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/
select proname from pg_proc where proname='u_testfun68';
--添加IF EXISTS 子句并且添加函数参数，删除已存在的函数，提示删除成功
drop FUNCTION if EXISTS u_testfun68(c_int int);
 --添加IF EXISTS 子句并且添加函数参数，删除函数，提示函数u_testfun68不存在，发出一个notice
 drop FUNCTION if EXISTS u_testfun68(c_int int);
