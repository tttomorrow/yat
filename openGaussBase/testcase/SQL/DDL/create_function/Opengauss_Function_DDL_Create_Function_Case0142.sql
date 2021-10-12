--  @testpoint:定义INOUT参数模式有两个，返回值不设为record，合理报错
drop FUNCTION if EXISTS x_testfun4;
CREATE FUNCTION x_testfun4 (c_int INOUT int,c_int1 INOUT int  ) returns int   AS $$
        BEGIN
                RETURN next;
        END;
$$ LANGUAGE plpgsql;
/