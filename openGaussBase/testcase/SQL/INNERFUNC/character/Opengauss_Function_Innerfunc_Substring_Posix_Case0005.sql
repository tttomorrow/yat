-- @testpoint: 字符串尾匹配
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('Thomas');
SELECT substring(string1 from  '...$') from type_char;
DROP TABLE IF EXISTS type_char;