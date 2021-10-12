-- @testpoint: 模式匹配POSIX正则表达式,使用[...]声明一个字符类
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(100));
insert into type_char values ('aabc');
SELECT * from type_char  where string1 ~ '[ab]';
DROP TABLE IF EXISTS type_char;