-- @testpoint: 搜索文本包含所有string字符
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('& xxxxTRIaM');
SELECT ltrim(string1,'& xxxxTRIaM') from type_char;
DROP TABLE IF EXISTS type_char;