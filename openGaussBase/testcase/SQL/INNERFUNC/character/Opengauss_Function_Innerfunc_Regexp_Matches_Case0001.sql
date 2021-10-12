-- @testpoint: 正常值匹配不到
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('foobarbequebaz');
SELECT regexp_matches(string1,'Thom') from type_char;
DROP TABLE IF EXISTS type_char;