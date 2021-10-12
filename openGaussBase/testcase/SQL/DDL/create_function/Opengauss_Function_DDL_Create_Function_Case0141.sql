--  @testpoint:定义INOUT参数模式有两个，返回值设为record
drop FUNCTION if EXISTS x_testfun2;
CREATE FUNCTION x_testfun2 (c_int INOUT int,c_int1 INOUT int  ) returns setof record   AS $$
        BEGIN
                RETURN next;
        END;
$$ LANGUAGE plpgsql;
/
call x_testfun2(999,9909);
drop FUNCTION x_testfun2;