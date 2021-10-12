--  @testpoint:创建函数指定参数模式是IN，proargtypes字段显示参数的数据类型
drop FUNCTION if EXISTS w_testfund;
CREATE FUNCTION w_testfund (c_int IN int )  RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/

select proname ,proargtypes from pg_proc where proname='w_testfund';
drop FUNCTION  w_testfund;