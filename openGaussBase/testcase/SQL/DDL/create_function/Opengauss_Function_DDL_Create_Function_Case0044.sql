DROP FUNCTION if EXISTS k_testfun5 (arg1 INOUT integer,arg2 VARIADIC int[]);
CREATE  FUNCTION k_testfun5 (arg1 INOUT integer,arg2 VARIADIC int[]) RETURNS integer AS $$
        BEGIN
                RETURN arg1 + 1;
        END;
$$ LANGUAGE plpgsql;
/
select proargmodes from pg_proc where proname='k_testfun5';
DROP FUNCTION k_testfun5;