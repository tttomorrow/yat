-- @testpoint: 只有一个参数，指定参数模式为OUT
DROP FUNCTION if EXISTS i_testfun1 (i integer);
    CREATE  FUNCTION i_testfun1 (i OUT integer) RETURNS integer AS $$
        BEGIN
                RETURN i + 1;
        END;
$$ LANGUAGE plpgsql;
/
call i_testfun1(999);
--查询pg_proc表，proargmodes字段的值为o，表示参数模式是OUT
select proargmodes from pg_proc where proname='i_testfun1';
drop function  i_testfun1;