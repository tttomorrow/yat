-- @testpoint: 正常值插入补齐空格
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (stringv char(20));
insert into type_char values ('ou mygod');
select bit_length(stringv) from type_char;
DROP TABLE IF EXISTS type_char;