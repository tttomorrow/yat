-- @testpoint: 字符串中找不到分隔字符
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('abc');
SELECT split_part(string1,'d',1) from type_char;
DROP TABLE IF EXISTS type_char;