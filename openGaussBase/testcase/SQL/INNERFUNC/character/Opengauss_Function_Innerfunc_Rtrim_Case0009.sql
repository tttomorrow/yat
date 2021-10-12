-- @testpoint: 空格处理、特殊字符
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('sdffxxx1% &');
SELECT rtrim(string1,' &%') from type_char;
DROP TABLE IF EXISTS type_char;