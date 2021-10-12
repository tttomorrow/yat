-- @testpoint: 有多个搜索字符时返回第一个位置
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (stringv char(20));
insert into type_char values ('stringing');
SELECT position('ing' in stringv) from type_char;
DROP TABLE IF EXISTS type_char;