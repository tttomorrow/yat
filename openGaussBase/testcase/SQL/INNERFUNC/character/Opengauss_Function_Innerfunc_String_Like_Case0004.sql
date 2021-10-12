-- @testpoint: 匹配字符为中文英文数字特殊符号
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('我是123AA@_BBCC');
SELECT  (string1 LIKE '%A@_B%') from type_char AS RESULT;
DROP TABLE IF EXISTS type_char;