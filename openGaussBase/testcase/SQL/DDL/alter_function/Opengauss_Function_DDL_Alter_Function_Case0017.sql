--  @testpoint:修改函数的调用null值方式
--创建函数指定参数RETURNS NULL ON NULL INPUT
drop FUNCTION if EXISTS test_func1(integer,integer);
CREATE FUNCTION test_func1(integer,integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
--修改参数RETURNS NULL ON NULL INPUT为ON NULL INPUT
ALTER FUNCTION test_func1(integer,integer) CALLED ON NULL INPUT;
--调用函数，参数含有null值，正常调用
call test_func1(null,66);
call test_func1('',66);
--调用函数，参数没有null值
call test_func1(88,66);


--修改为原来的参数RETURNS NULL ON NULL INPUT
ALTER FUNCTION test_func1(integer,integer) RETURNS NULL ON NULL INPUT;
--调用函数，参数含有null值，结果返回null
call test_func1('',66);
call test_func1(null,66);
 call test_func1(null,null);
 --调用函数，参数没有null值
 call test_func1(88,66);


 --修改RETURNS NULL ON NULL INPUT为STRICT
 ALTER FUNCTION test_func1(integer,integer) STRICT;
 --调用函数，参数含有null值，结果返回null
call test_func1('',66);
call test_func1(null,66);
 call test_func1(null,null);
 --调用函数，参数没有null值
 call test_func1(88,66);
 drop function test_func1 (integer,integer);