--  @testpoint:创建函数给参数指定默认值，使用=
drop FUNCTION if EXISTS w_testfun8;
CREATE FUNCTION w_testfun8 (c_int int = 2)  RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/
--调用函数，给参数不传值，使用默认值
call  w_testfun8();
--调用函数，给参数传值，使用新值
call  w_testfun8(999);
drop FUNCTION w_testfun8;