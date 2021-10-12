--  @testpoint:省略函数的参数名
drop function if exists fun_test2(int1, int1);
CREATE FUNCTION fun_test2(int1, int1) RETURNS double precision
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
select proargnames from pg_proc where proname='fun_test2';
call fun_test2(10,10);
drop FUNCTION fun_test2;