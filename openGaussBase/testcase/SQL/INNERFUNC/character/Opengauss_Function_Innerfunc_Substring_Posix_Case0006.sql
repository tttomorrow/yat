-- @testpoint: 字符串带括号匹配
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('Thomas');
SELECT substring(string1 from  'o(..)s') from type_char;
DROP TABLE IF EXISTS type_char;