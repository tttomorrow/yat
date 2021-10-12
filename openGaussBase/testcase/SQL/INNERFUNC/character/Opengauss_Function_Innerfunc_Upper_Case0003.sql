-- @testpoint: 数据类型不是字符
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 int);
insert into type_char values (111);
SELECT upper(string1) from type_char;
DROP TABLE IF EXISTS type_char;