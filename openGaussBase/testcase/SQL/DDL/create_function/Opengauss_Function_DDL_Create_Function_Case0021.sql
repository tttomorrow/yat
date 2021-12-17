--  @testpoint:函数名长度测试
drop function if exists "abcdefghijklmnopqrstuvwxyz1234567891234567891234567891234567891a";
CREATE FUNCTION "abcdefghijklmnopqrstuvwxyz1234567891234567891234567891234567891a"(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
select proname from pg_proc where proname='abcdefghijklmnopqrstuvwxyz1234567891234567891234567891234567891a';
drop function "abcdefghijklmnopqrstuvwxyz1234567891234567891234567891234567891a";
