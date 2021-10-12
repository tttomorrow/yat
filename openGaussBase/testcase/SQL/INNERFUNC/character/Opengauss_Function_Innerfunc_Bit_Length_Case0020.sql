-- @testpoint: 正常值插入为‘’
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (stringv char);
insert into type_char values ('');
select bit_length(stringv) from type_char;
DROP TABLE IF EXISTS type_char;