-- @testpoint: 不存在的列,合理报错
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 int);
insert into type_char values (111);
SELECT quote_ident(string11) from type_char;
DROP TABLE IF EXISTS type_char;