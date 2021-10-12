-- @testpoint: 大小写匹配
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('str');
SELECT regexp_substr(string1 ,'[St][r]') from type_char;
DROP TABLE IF EXISTS type_char;