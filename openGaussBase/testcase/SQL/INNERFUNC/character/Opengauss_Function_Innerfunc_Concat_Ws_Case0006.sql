-- @testpoint: 只有分隔符其他参数全缺失，合理报错
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values (concat_ws(' '));
SELECT * from type_char;
DROP TABLE IF EXISTS type_char;