--  @testpoint:opengauss关键字Language(非保留)，定义函数为SQL查询

drop function  if exists func_add_sql;
	
CREATE FUNCTION func_add_sql(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
	
select * from func_add_sql(1,3);
drop function func_add_sql;
	

	
drop function if exists func_dup_sql;
CREATE FUNCTION func_dup_sql(in int, out f1 int, out f2 text)
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    LANGUAGE SQL;
/
SELECT * FROM func_dup_sql(42);
drop function func_dup_sql;

