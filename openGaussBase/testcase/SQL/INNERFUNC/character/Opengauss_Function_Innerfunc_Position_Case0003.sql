-- @testpoint: 大小写匹配
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (stringv char(20));
insert into type_char values ('stringing');
SELECT position('ING' in stringv) from type_char;
DROP TABLE IF EXISTS type_char;