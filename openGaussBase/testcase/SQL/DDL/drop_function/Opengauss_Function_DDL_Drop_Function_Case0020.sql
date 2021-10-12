-- @testpoint: 删除函数，添加模式名删除（模式名不存在）,合理报错
drop FUNCTION if EXISTS u_testfun89(c_int int);
CREATE FUNCTION u_testfun89 ( INOUT c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/
--删除函数，添加模式名删除
drop FUNCTION dy.u_testfun89;
--删除函数，不加模式名
drop FUNCTION u_testfun89;