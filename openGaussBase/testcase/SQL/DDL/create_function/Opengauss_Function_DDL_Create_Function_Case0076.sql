-- @testpoint: 创建函数给参数指定参数模式为INOUT并且指定默认值，使用DEFAULT 合理报错
drop FUNCTION if EXISTS w_testfun3;
CREATE FUNCTION w_testfun3 (c_int INOUT int DEFAULT  1)  RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/
--调用函数，给参数不传值，使用默认值
call  w_testfun3();
--调用函数，给参数传值，使用新值
call  w_testfun3(999);