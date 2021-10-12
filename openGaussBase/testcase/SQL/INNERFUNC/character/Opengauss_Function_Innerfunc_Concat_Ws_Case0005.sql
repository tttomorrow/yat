-- @testpoint: 第二个参数之后都是null
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values (concat_ws(' ', null,null,null));
SELECT * from type_char;
DROP TABLE IF EXISTS type_char;