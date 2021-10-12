--  @testpoint:创建函数指定参数的数据类型是int型，默认值取date型，合理报错
drop FUNCTION if EXISTS w_testfun0;
CREATE FUNCTION w_testfun0 (c_int int ='2020-08-10')  RETURNS date  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/