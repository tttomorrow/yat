--  @testpoint:创建函数，指定参数模式是INOUT，省略RETURNS子句
drop FUNCTION if EXISTS x_testfun3;
CREATE FUNCTION x_testfun3 (c_int INOUT int   )    AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/
call x_testfun3(999);
drop FUNCTION x_testfun3;