--  @testpoint:创建函数时指定参数EXTERNAL SECURITY INVOKER
drop FUNCTION if EXISTS v_testfun4(c_int int);
CREATE FUNCTION v_testfun4 (c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql
STRICT
EXTERNAL SECURITY INVOKER;
/

call v_testfun4(999);
drop FUNCTION v_testfun4;
