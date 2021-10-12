-- @testpoint: 模式匹配操作符LIKE,使用_匹配
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(100));
insert into type_char values ('abcd');
SELECT * from type_char  where string1 LIKE 'ab_d';
SELECT * from type_char  where string1 LIKE 'abc_';
SELECT * from type_char  where string1 LIKE '_bc_';
DROP TABLE IF EXISTS type_char;