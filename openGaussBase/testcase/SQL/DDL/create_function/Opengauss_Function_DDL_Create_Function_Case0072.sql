--  @testpoint:创建函数给参数指定默认值，使用DEFAULT，缺省表达式的数据类型和参数类型不匹配，合理报错
drop FUNCTION if EXISTS w_testfun6;
CREATE FUNCTION w_testfun6 (c_int int  DEFAULT  'true')  RETURNS BOOLEAN  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/