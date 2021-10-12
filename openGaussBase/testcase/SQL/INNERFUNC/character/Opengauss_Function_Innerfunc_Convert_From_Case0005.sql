-- @testpoint: 缺参数，合理报错
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values (convert_from('是sA@#123'));
SELECT * from type_char;
DROP TABLE IF EXISTS type_char;