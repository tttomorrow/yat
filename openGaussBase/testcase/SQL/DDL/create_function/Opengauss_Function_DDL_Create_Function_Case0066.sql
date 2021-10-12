--  @testpoint:创建函数指定参数数据类型是特殊字符类型
drop FUNCTION if EXISTS y_testfun5;
CREATE FUNCTION y_testfun5 (c_name name,c_char "char") RETURNS name  AS $$
        BEGIN
                RETURN (c_name,c_char);
        END;
$$ LANGUAGE plpgsql;
/
--"char"只存储1字节
call y_testfun5('abc','helloworld');
drop FUNCTION y_testfun5;