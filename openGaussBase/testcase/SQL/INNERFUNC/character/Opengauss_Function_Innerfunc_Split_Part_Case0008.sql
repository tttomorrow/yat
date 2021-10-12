-- @testpoint: 中文
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('我是一个');
SELECT split_part(string1,'是',1) from type_char;
DROP TABLE IF EXISTS type_char;