--  @testpoint:创建函数，给两个参数都取默认值
drop FUNCTION if EXISTS x_testfun0;
CREATE FUNCTION x_testfun0 (c_int int =2020,c_char char DEFAULT 'gauss')  RETURNS char  AS $$
        BEGIN
                RETURN (c_int,c_char);
        END;
$$ LANGUAGE plpgsql;
/
--调用函数，给参数不传值，使用默认值
call x_testfun0();
--调用函数，给第一个参数传值，第二个参数使用默认值
call x_testfun0(0813);
--调用函数，给两个函数都传入新值
call x_testfun0(666,'world');
drop FUNCTION x_testfun0;