-- @testpoint: 与时间函数连接
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values (concat_ws('，', 'ABCDE', 2017-1-7));
SELECT * from type_char;
DROP TABLE IF EXISTS type_char;