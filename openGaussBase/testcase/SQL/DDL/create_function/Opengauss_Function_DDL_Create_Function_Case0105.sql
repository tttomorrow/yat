--  @testpoint:创建函数，指定参数SECURITY DEFINER
drop FUNCTION if EXISTS v_testfun7(c_int int);
CREATE FUNCTION v_testfun7 (c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql
STRICT
SECURITY DEFINER;
/

call v_testfun7(999);
drop FUNCTION v_testfun7;