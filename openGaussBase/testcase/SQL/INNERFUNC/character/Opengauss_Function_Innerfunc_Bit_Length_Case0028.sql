-- @testpoint: 正常值插入TEXT

DROP TABLE IF EXISTS type_nchar2;
CREATE TABLE type_nchar2 (stringv TEXT);
insert into type_nchar2 values ('ou mygod中>%');
select bit_length(stringv) from type_nchar2;
DROP TABLE IF EXISTS type_nchar2;