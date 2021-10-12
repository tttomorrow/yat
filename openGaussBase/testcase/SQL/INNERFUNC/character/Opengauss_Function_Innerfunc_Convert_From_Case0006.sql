-- @testpoint: 备转换值为空值
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values (convert_from('', 'UTF8'));
SELECT * from type_char;
DROP TABLE IF EXISTS type_char;