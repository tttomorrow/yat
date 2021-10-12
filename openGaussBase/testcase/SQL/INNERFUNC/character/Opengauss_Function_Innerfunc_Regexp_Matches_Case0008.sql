-- @testpoint: 字符串为空
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('');
SELECT regexp_matches(string1,'[A-z]','g') from type_char;
DROP TABLE IF EXISTS type_char;