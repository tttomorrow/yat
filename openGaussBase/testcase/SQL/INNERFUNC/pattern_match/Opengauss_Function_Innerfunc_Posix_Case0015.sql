-- @testpoint: 模式匹配POSIX正则表达式,对数字进行匹配
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 int);
insert into type_char values (123456);
SELECT * from type_char  where string1 ~ '[0-9]';
DROP TABLE IF EXISTS type_char;