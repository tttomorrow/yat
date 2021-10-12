-- @testpoint: 被搜索字符为空
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('');
SELECT strpos(string1,'rc') from type_char;
DROP TABLE IF EXISTS type_char;