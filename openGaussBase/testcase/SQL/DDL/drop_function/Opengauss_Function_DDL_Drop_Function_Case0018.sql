--  @testpoint:删除已存在的函数，省略IF EXISTS 子句并且省略函数参数，删除成功后再次执行删除语句，后者报错
drop FUNCTION if EXISTS u_testfun88(c_int int);
CREATE FUNCTION u_testfun88 ( INOUT c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/

select proname from pg_proc where proname='u_testfun88';
--只添加函数名删除函数
drop FUNCTION  u_testfun88;
--再次执行删除操作，报错提示函数u_testfun88不存在
drop FUNCTION  u_testfun88;