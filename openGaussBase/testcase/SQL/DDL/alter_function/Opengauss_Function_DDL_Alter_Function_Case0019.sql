--  @testpoint:修改函数的返回函数
--创建返回不是集合的函数
drop FUNCTION if EXISTS test_func1(integer,integer);
CREATE FUNCTION test_func1(integer,integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT
    cost 100;
    /
 --修改函数的返回行数是20，合理报错
 ALTER FUNCTION test_func1(integer,integer) rows 20;
 drop function test_func1(integer,integer);


 --创建返回集合的函数
 drop FUNCTION if EXISTS compute (i int, out result_1 bigint, out result_2 bigint);
 CREATE  FUNCTION compute(i int, out result_1 bigint, out result_2 bigint)
returns SETOF RECORD
as $$
begin
    result_1 = i + 1;
    result_2 = i * 10;
return next;
end;
$$language plpgsql
rows 5;
/
--修改返回行数是4
alter function compute(i int, out result_1 bigint, out result_2 bigint) rows 4;
--修改返回行数是0，合理报错
alter function compute(i int, out result_1 bigint, out result_2 bigint) rows 0;
--修改返回行数是-4，合理报错
alter function compute(i int, out result_1 bigint, out result_2 bigint) rows 0;
--修改返回行数是非数字，合理报错
alter function compute(i int, out result_1 bigint, out result_2 bigint) rows 2$;
drop FUNCTION test_func1(integer,integer);
