--  @testpoint:修改函数的模式,新模式不存在，合理报错
drop FUNCTION if EXISTS u_testfun59(c_int int);
CREATE FUNCTION u_testfun59 ( INOUT c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/

ALTER FUNCTION u_testfun59(c_int int) SET SCHEMA cjhs;
drop FUNCTION u_testfun59;