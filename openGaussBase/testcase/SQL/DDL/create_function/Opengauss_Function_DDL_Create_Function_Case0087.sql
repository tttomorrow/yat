--  @testpoint:返回一个包含多个输出参数的记录
drop FUNCTION if EXISTS func_dup_sql;
CREATE FUNCTION func_dup_sql(in int, out f1 int, out f2 text)
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    LANGUAGE SQL;
/
SELECT * FROM func_dup_sql(42);
drop FUNCTION func_dup_sql;