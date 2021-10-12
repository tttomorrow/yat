-- @testpoint: 参数不为字符串
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 int);
insert into type_char values (123);
SELECT ltrim(string1,1) from type_char;
DROP TABLE IF EXISTS type_char;