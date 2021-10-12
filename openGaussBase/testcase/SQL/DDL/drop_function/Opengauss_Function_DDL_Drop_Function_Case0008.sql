--  @testpoint:删除函数添加CASCADE参数且添加函数参数
drop FUNCTION if EXISTS u_testfun76(c_int int)cascade;
CREATE FUNCTION u_testfun76 ( INOUT c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/
select proname from pg_proc where proname='u_testfun76';
--添加IF EXISTS 子句，删除已存在的函数并且添加CASCADE参数
drop FUNCTION u_testfun76(c_int int) cascade;