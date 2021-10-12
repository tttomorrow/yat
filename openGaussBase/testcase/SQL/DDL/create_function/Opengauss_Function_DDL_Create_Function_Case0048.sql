--  @testpoint:只有一个参数，指定参数模式是IN
    DROP FUNCTION if EXISTS g_testfun1 (i  IN integer);
    CREATE  FUNCTION g_testfun1 (i IN integer) RETURNS integer AS $$
        BEGIN
                RETURN i + 1;
        END;
$$ LANGUAGE plpgsql;
/
--查询pg_proc表，proargmodes字段的值为空，即表示是IN模式
select proargmodes from pg_proc where proname='g_testfun1';
drop function  g_testfun1;