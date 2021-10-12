--  @testpoint:OUT参数模式后跟VARIADIC模式，函数创建成功
DROP FUNCTION if EXISTS k_testfun6 (arg1 OUT integer,arg2 VARIADIC int[]);
CREATE  FUNCTION k_testfun6 (arg1 OUT integer,arg2 VARIADIC int[]) RETURNS integer AS $$
        BEGIN
                RETURN arg1 + 1;
        END;
$$ LANGUAGE plpgsql;
/
select proargmodes from pg_proc where proname='k_testfun6';
DROP FUNCTION k_testfun6;