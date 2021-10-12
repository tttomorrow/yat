-- @testpoint: 没有搜索字符
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (stringv char(20));
insert into type_char values ('stringing');
SELECT position('' in stringv) from type_char;
DROP TABLE IF EXISTS type_char;