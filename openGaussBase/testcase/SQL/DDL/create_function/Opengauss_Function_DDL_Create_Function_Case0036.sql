--  @testpoint:只有一个参数，并且不指定参数模式，测试函数参数模式默认值是否为IN
    DROP FUNCTION if EXISTS g_testfun (i integer);
    CREATE  FUNCTION g_testfun (i integer) RETURNS integer AS $$
        BEGIN
                RETURN i + 1;
        END;
$$ LANGUAGE plpgsql;
/
--查询pg_proc表，proargmodes字段的值为空，即默认是IN模式
select proargmodes from pg_proc where proname='g_testfun';
drop function  g_testfun;