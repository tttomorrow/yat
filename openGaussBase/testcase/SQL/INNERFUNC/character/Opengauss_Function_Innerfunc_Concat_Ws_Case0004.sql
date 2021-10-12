-- @testpoint: 特殊符号、汉字英文数字
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values (concat_ws(' ', 'ABCDE',1,null));
SELECT * from type_char;
DROP TABLE IF EXISTS type_char;