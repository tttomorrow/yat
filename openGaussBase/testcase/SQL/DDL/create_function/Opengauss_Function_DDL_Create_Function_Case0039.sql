--  @testpoint:函数参数有三个，全部指定参数模式为OUT
DROP FUNCTION if EXISTS j_testfun1 (i OUT integer,j OUT integer,k OUT integer);
    CREATE  FUNCTION j_testfun1 (i OUT integer,j OUT integer,k OUT integer) RETURNS integer AS $$
        BEGIN
                RETURN i + j+k;
        END;
$$ LANGUAGE plpgsql;
/
--查询pg_proc表proargmodes字段是{o,o,o}，即三个参数的模式都是OUT

select proargmodes from pg_proc where proname='j_testfun1';
drop function  j_testfun1;