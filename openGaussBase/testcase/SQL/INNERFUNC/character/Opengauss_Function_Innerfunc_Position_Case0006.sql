-- @testpoint: 中文检索
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (stringv char(20));
insert into type_char values ('我是中国');
SELECT position('我' in stringv) from type_char;
DROP TABLE IF EXISTS type_char;