-- @testpoint: 不能进行相互转换的编码
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values (convert_to('some text', 'GBK'));
SELECT * from type_char;
DROP TABLE IF EXISTS type_char;