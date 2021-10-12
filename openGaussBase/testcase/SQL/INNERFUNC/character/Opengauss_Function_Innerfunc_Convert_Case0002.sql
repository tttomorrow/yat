-- @testpoint: 中文特殊符号数字英文正常转换
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values (convert('是sA@#123', 'UTF8', 'GBK' ));
SELECT * from type_char;
DROP TABLE IF EXISTS type_char;