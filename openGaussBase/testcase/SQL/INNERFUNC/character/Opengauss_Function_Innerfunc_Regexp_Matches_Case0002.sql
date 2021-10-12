-- @testpoint: 中文匹配
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('我是一个');
SELECT regexp_matches(string1,'是') from type_char;
DROP TABLE IF EXISTS type_char;