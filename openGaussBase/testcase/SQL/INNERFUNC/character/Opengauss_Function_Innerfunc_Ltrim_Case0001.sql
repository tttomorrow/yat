-- @testpoint: 第一位不是搜索字符
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('xxxxTRIM');
SELECT ltrim(string1,'a') from type_char;
DROP TABLE IF EXISTS type_char;