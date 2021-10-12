--  @testpoint:函数名由数字，字母，美元符号（$）组成，创建成功
drop function if exists func_test1$(integer, integer);
CREATE FUNCTION func_test1$(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
select proname from pg_proc where proname='func_test1$';
drop FUNCTION func_test1$;