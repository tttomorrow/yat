-- @testpoint: 多个括号
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('str');
SELECT regexp_substr(string1 ,'[st][r]') from type_char;
DROP TABLE IF EXISTS type_char;