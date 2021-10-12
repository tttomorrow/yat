--  @testpoint:创建函数时省略CALLED ON NULL INPUT
drop FUNCTION if EXISTS v_testfun1(c_int int);
CREATE FUNCTION v_testfun1 (c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/

--调用函数，指定参数值null，可以按照正常的方式调用
call v_testfun1(null);
drop FUNCTION v_testfun1;
