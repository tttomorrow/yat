--  @testpoint:修改函数的模式
drop FUNCTION if EXISTS u_testfun55(c_int int);
CREATE FUNCTION u_testfun55 ( INOUT c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/
--创建hs模式
drop schema if EXISTS hs cascade;
create schema hs;
--修改函数模式
ALTER FUNCTION u_testfun55(c_int int) SET SCHEMA hs;
--查询函数信息
select proargnames,proname from pg_proc where proname='u_testfun55';
--清理环境
drop FUNCTION hs.u_testfun55;
drop schema hs;