-- @testpoint: 搜索字符多于1个
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('xxxxTRIaM');
SELECT ltrim(string1,'xT') from type_char;
DROP TABLE IF EXISTS type_char;