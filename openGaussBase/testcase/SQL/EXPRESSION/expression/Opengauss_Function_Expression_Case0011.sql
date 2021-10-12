-- @testpoint: COALESCE 合理报错
--COALESCE返回它的第一个非NULL的参数值。如果参数都为NULL，则返回NULL。
--它常用于在显示数据时用缺省值替换NULL。和CASE表达式一样，COALESCE只计算用来判断结果的参数，即在第一个非空参数右边的参数不会被计算

DROP TABLE if exists test_expression_11 cascade;
CREATE TABLE test_expression_11(description varchar(10), short_description varchar(10), last_value varchar(10)) ;
INSERT INTO test_expression_11 VALUES('abc', 'efg', '123');
INSERT INTO test_expression_11 VALUES(NULL, 'efg', '123');
INSERT INTO test_expression_11 VALUES(NULL, NULL, '123');
SELECT description, short_description, last_value, COALESCE(description, short_description, last_value) FROM test_expression_11 ORDER BY 1, 2, 3, 4;

--如果description不为NULL，则返回description的值，否则计算下一个参数short_description；
--如果short_description不为NULL，则返回short_description的值，否则计算下一个参数last_value；
--如果last_value不为NULL，则返回last_value的值，否则返回（none）。

--无参
SELECT COALESCE();

--1参
SELECT COALESCE(NULL);
SELECT COALESCE('test');
SELECT COALESCE(1);
SELECT COALESCE(1::int);
SELECT COALESCE('test'::varchar);
SELECT COALESCE('test'::clob);
SELECT COALESCE('test'::text);
SELECT COALESCE('3 days'::reltime);
SELECT COALESCE('false'::boolean);
SELECT COALESCE(inet '0.0.5.0/24'::cidr);
SELECT COALESCE(lseg '(1,2),(3,2)');

--多参含有null
SELECT COALESCE(NULL,'Hello World','test','expression');
SELECT COALESCE('Hello World','test',NULL,'expression');
SELECT COALESCE('Hello World','test','expression',NULL);
SELECT COALESCE(NULL,NULL,NULL,'expression');

--清理环境
DROP TABLE if exists test_expression_11 cascade;
