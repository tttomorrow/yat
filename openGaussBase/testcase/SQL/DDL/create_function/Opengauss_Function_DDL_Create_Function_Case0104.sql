--  @testpoint:创建函数指定参数AUTHID CURRENT_USER
 drop FUNCTION if EXISTS v_testfun5(c_int int);
CREATE FUNCTION v_testfun5 (c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql
STRICT
AUTHID CURRENT_USER;
 /
 call v_testfun5(100);
 drop FUNCTION v_testfun5;

