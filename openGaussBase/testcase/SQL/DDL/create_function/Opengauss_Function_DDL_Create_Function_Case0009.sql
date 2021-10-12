--  @testpoint:创建函数不指定模式名（在当前schema下）
SELECT CURRENT_SCHEMA;
drop FUNCTION if EXISTS add_two(integer, integer);
CREATE FUNCTION add_two(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
 /
 select proname from pg_proc where proname='add_two';
 drop FUNCTION add_two;