-- @testpoint: 括号为空,合理报错
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('str');
SELECT regexp_substr(string1 ,'[]') from type_char;
DROP TABLE IF EXISTS type_char;