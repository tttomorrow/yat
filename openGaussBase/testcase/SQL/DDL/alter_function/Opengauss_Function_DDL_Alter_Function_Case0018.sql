--  @testpoint:修改函数的cost参数
--创建函数指定cost是100
drop FUNCTION if EXISTS test_func1(integer,integer);
CREATE FUNCTION test_func1(integer,integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT
    cost 100;
    /
--修改函数的cost是150
 ALTER FUNCTION test_func1(integer,integer) cost 150;
--修改函数的cost是0，合理报错
 ALTER FUNCTION test_func1(integer,integer) cost 0;
--修改函数的cost是-150，合理报错
 ALTER FUNCTION test_func1(integer,integer) cost -150;
--修改函数的cost是非数字，合理报错
 ALTER FUNCTION test_func1(integer,integer) cost 20$;
 drop function test_func1(integer,integer);