-- @testpoint: 模式匹配操作符LIKE,字符串与模式相等
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(100));
insert into type_char values ('abc');
SELECT * from type_char  where string1 LIKE 'abc';
DROP TABLE IF EXISTS type_char;