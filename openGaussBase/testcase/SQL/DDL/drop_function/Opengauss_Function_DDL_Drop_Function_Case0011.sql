--  @testpoint:删除函数添加RESTRICT参数并且省略函数参数
drop FUNCTION if EXISTS u_testfun95(int)  RESTRICT;
CREATE FUNCTION u_testfun95 ( INOUT c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/
--删除函数添加RESTRICT参数并且省略函数参数类型，合理报错
drop FUNCTION if EXISTS u_testfun95  RESTRICT;
--删除函数添加RESTRICT参数并且添加类型，删除成功
drop FUNCTION if EXISTS u_testfun95 ( int)RESTRICT;