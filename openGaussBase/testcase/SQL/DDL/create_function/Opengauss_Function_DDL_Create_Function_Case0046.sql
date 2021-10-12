DROP FUNCTION if EXISTS k_testfun7 (arg1 IN integer,arg2 VARIADIC int[]);
CREATE  FUNCTION k_testfun7 (arg1 IN integer,arg2 VARIADIC int[]) RETURNS integer AS $$
        BEGIN
                RETURN arg1 + 1;
        END;
$$ LANGUAGE plpgsql;
/
select proargmodes from pg_proc where proname='k_testfun7';
DROP FUNCTION k_testfun7;