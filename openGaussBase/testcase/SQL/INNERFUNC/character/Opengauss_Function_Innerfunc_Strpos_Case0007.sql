-- @testpoint: 字符串= 检索字符
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('source');
SELECT strpos(string1,'source') from type_char;
DROP TABLE IF EXISTS type_char;