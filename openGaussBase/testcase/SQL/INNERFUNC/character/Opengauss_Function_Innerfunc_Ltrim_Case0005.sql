-- @testpoint: 最后一个参数不为字符为数字
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('xxxxTRIaM');
SELECT ltrim(string1,1) from type_char;
DROP TABLE IF EXISTS type_char;