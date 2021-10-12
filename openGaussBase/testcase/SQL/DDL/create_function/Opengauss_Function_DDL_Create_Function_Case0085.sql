--  @testpoint:创建函数，指定参数模式是VARIADIC，省略RETURNS子句,合理报错
drop FUNCTION if EXISTS x_testfun5;
CREATE FUNCTION x_testfun5 (c_int  VARIADIC int[]   )    AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/