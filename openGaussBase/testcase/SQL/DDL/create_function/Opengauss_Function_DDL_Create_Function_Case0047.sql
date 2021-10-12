--  @testpoint:定义两个参数模式都是VARIADIC模式，合理报错
DROP FUNCTION if EXISTS k_testfun8 (arg1 VARIADIC int[] ,arg2 VARIADIC int[]);
CREATE  FUNCTION k_testfun7 (arg1 VARIADIC int[],arg2 VARIADIC int[]) RETURNS integer AS $$
        BEGIN
                RETURN arg1 + 1;
        END;
$$ LANGUAGE plpgsql;
/