-- @testpoint: 分隔符=字符串
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('abc');
SELECT split_part(string1,'abc',1) from type_char;
SELECT split_part(string1,'abc',2) from type_char;
DROP TABLE IF EXISTS type_char;