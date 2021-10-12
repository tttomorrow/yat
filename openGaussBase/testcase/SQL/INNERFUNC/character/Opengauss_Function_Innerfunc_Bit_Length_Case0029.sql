-- @testpoint: 入参为 ''
DROP TABLE IF EXISTS type_nchar2;
CREATE TABLE type_nchar2 (stringv TEXT);
insert into type_nchar2 values ('');
select bit_length(stringv) from type_nchar2;
DROP TABLE IF EXISTS type_nchar2;