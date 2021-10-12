--  @testpoint:创建函数，指定参数模式是OUT，省略RETURNS子句（OUT出参，调用时给的值不起作用）
drop FUNCTION if EXISTS x_testfun2;
CREATE FUNCTION x_testfun2 (c_int OUT int   )    AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/
call x_testfun2(999);
drop FUNCTION x_testfun2;