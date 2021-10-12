--  @testpoint: 创建函数时使用AUTHID，应该报错
drop FUNCTION if EXISTS v_testfun5(c_int int);
CREATE FUNCTION v_testfun5 (c_int int) AUTHID RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql
STRICT
AUTHID ;
 /