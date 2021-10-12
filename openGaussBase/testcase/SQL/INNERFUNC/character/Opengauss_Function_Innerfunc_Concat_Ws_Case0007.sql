-- @testpoint: 与json串连接
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values (concat_ws('，', 'ABCDE', '{"f1":1,"f2":true,"f3":"Hi"}'));
SELECT * from type_char;
DROP TABLE IF EXISTS type_char;