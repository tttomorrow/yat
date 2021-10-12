-- @testpoint: 模式匹配操作符LIKE,使用NOT LIKE为整串匹配
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(100));
insert into type_char values ('abc');
SELECT * from type_char  where string1 NOT LIKE 'a';
SELECT * from type_char  where string1 NOT LIKE 'abc';
DROP TABLE IF EXISTS type_char;