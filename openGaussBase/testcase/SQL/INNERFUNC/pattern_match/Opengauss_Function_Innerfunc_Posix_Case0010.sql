-- @testpoint: 模式匹配POSIX正则表达式,使用$自串尾匹配
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(10));
insert into type_char values ('abc');
SELECT * from type_char  where string1 ~ 'c$';
SELECT * from type_char  where string1 ~ '$';
SELECT * from type_char  where string1 ~ '(abc)$';
DROP TABLE IF EXISTS type_char;