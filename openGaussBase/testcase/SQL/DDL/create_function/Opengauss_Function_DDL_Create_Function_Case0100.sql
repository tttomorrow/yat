--  @testpoint:创建函数时指定参数RETURNS NULL ON NULL INPUT
drop FUNCTION if EXISTS v_testfun2(c_int int);
CREATE FUNCTION v_testfun2 (c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql
RETURNS NULL ON NULL INPUT;
/


call v_testfun2(null);
drop FUNCTION v_testfun2;