-- @testpoint: 大小写匹配
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('sourcercRC');
SELECT strpos(string1,'rc') from type_char;
DROP TABLE IF EXISTS type_char;