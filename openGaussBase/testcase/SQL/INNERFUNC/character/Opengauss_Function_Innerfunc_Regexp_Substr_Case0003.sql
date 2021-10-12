-- @testpoint: 不带括号中文特殊符号匹配
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('str中文￥&*');
SELECT regexp_substr(string1 ,'str中文￥&*') from type_char;
DROP TABLE IF EXISTS type_char;