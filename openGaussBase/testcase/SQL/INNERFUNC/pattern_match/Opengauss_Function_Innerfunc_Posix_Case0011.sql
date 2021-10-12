-- @testpoint: 模式匹配POSIX正则表达式,使用.匹配任意单个字符
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(10));
insert into type_char values ('abc');
SELECT * from type_char  where string1 ~ '.$';
SELECT * from type_char  where string1 ~ '.b.$';
DROP TABLE IF EXISTS type_char;