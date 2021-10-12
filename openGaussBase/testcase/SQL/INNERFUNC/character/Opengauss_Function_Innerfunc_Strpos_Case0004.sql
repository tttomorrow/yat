-- @testpoint: 检索字为空格、为空
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('sourcercRC');
SELECT strpos(string1,'') from type_char;
SELECT strpos(string1,' ') from type_char;
DROP TABLE IF EXISTS type_char;