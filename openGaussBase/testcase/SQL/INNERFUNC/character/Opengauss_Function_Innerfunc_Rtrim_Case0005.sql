-- @testpoint: 搜索文本是被搜索串的末尾字符
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('sdffxxx');
SELECT rtrim(string1,'xx') from type_char;
DROP TABLE IF EXISTS type_char;