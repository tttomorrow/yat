--  @testpoint:创建函数指定参数模式是OUT模式，proargtypes字段不显示
drop FUNCTION if EXISTS w_testfuna;
CREATE FUNCTION w_testfuna (c_int OUT int )  RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/

select proname,proargtypes from pg_proc where proname='w_testfuna';
drop FUNCTION  w_testfuna;