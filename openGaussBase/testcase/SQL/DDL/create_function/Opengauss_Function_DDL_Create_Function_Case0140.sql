--  @testpoint:定义OUT参数模式有两个，返回值不设为record，合理报错
drop FUNCTION if EXISTS x_testfun4;
CREATE FUNCTION x_testfun4 (c_int OUT int,c_int1 OUT int  ) returns int   AS $$
        BEGIN
                RETURN next;
        END;
$$ LANGUAGE plpgsql;
/
