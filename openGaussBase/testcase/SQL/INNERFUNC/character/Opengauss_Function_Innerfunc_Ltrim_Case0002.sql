-- @testpoint: 字符串的非首位有该字符
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('xxxxTRIaM');
SELECT ltrim(string1,'a') from type_char;
DROP TABLE IF EXISTS type_char;