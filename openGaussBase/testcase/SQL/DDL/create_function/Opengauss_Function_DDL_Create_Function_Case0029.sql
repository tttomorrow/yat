drop function if exists t_func9( "参数1" integer, "参数2" integer);
CREATE FUNCTION t_func9( "参数1" integer,"参数2" integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
 /
select proargnames from pg_proc where proname='t_func9';
call t_func9(999,1);
drop FUNCTION t_func9;