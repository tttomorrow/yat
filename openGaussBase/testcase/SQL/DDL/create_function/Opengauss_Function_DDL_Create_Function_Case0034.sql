--  @testpoint:函数的参数名长度测试（超过64位截断，资料未说明）

drop function if exists e_func5(abcdefghijklmnopqrstuvwxyz123456789123456789123456789123456789ab integer,abcdefghijklmnopqrstuvwxyz123456789123456789123456789123456789cd integer);
CREATE FUNCTION e_func5(abcdefghijklmnopqrstuvwxyz123456789123456789123456789123456789ab integer,abcdefghijklmnopqrstuvwxyz123456789123456789123456789123456789cd integer) RETURNS integer
    AS 'select $1 *$2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
select proargnames from pg_proc where proname='e_func5';
call e_func5 (999,0);
drop function e_func5;