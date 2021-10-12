--  @testpoint:创建函数时指定参数STRICT
drop FUNCTION if EXISTS v_testfun3(c_int int);
CREATE FUNCTION v_testfun3 (c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql
STRICT;
/

call v_testfun3(null);
drop FUNCTION v_testfun3;