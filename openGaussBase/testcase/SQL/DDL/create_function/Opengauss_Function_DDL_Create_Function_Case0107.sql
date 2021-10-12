--  @testpoint:创建函数，指定参数AUTHID DEFINER
drop FUNCTION if EXISTS v_testfun8(c_int int);
CREATE FUNCTION v_testfun8 (c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql
STRICT
AUTHID DEFINER ;
/

call v_testfun8(999);
drop FUNCTION v_testfun8;

