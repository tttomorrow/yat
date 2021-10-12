--  @testpoint:函数参数名由数字，字母，美元符号（$）组成
drop function if exists b_test1(func_test1$  integer, func_test2$ integer);
CREATE FUNCTION b_test1(func_test1$ integer, func_test2$ integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
select proargnames from pg_proc where proname='b_test1';
call b_test1(1,999);
drop FUNCTION b_test1;