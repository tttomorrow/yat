-- @testpoint: 空字符重复
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
SELECT repeat(string1,2) from type_char;
DROP TABLE IF EXISTS type_char;