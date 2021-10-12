--  @testpoint:创建函数给参数指定参数模式为OUT并且使用:=指定默认值，合理报错，出参不能取默认值
drop FUNCTION if EXISTS w_testfun2;
CREATE FUNCTION w_testfun2 (c_int OUT int :=1)  RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/
