--  @testpoint:只有一个参数，指定参数模式为VARIADIC且参数类型是数组类型，定义成功
DROP FUNCTION if EXISTS k_testfun2 (arg1 VARIADIC int[]);
CREATE  FUNCTION k_testfun2 (arg1 VARIADIC int[]) RETURNS int[] AS $$
        BEGIN
                RETURN arg1 + 1;
        END;
$$ LANGUAGE plpgsql;
/
select proargmodes from pg_proc where proname='k_testfun2';
drop function  k_testfun2;