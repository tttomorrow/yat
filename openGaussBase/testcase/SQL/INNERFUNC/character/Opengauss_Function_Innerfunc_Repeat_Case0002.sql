-- @testpoint: 重复0次
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('abcdeF中国@#￥');
SELECT repeat(string1,0) from type_char;
DROP TABLE IF EXISTS type_char;