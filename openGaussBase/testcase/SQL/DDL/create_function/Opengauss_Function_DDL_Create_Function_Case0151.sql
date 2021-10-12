-- @testpoint: 创建复合数据类型用于函数返回值中
--创建复合数据类型dup_result
drop type if exists dup_result cascade;
CREATE TYPE dup_result AS (f1 int, f2 text);
--创建函数
CREATE FUNCTION dup(int) RETURNS dup_result
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    LANGUAGE SQL;
/
--调用函数
 call dup(42);
 drop FUNCTION dup(int);
 drop type dup_result cascade;