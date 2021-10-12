--  @testpoint:创建函数指定参数模式是VARIADIC，proargtypes字段显示参数的数据类型
drop FUNCTION if EXISTS w_testfune;
CREATE FUNCTION w_testfune (c_int VARIADIC int[] )  RETURNS int[]  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/

select proname,proargtypes from pg_proc where proname='w_testfune';
drop FUNCTION  w_testfune;