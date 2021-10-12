-- @testpoint: 删除函数，添加模式名删除（模式名已存在）
drop FUNCTION if EXISTS u_testfun89(c_int int);
CREATE FUNCTION u_testfun89 ( INOUT c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/


drop SCHEMA if EXISTS dy;
create SCHEMA dy;
ALTER FUNCTION u_testfun89 ( INOUT c_int int) SET SCHEMA  dy;
drop FUNCTION dy.u_testfun89;
drop SCHEMA dy;