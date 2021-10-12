-- @testpoint: 模式匹配POSIX正则表达式,使用~及$匹配中文字符
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(100));
insert into type_char values ('我是一个');
SELECT * from type_char  where string1 ~ '个$';
DROP TABLE IF EXISTS type_char;