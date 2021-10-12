-- @testpoint: 正常值插入CHARACTER

DROP TABLE IF EXISTS type_nchar2;
CREATE TABLE type_nchar2 (stringv CHARACTER(20));
insert into type_nchar2 values ('ou mygod');
select bit_length(stringv) from type_nchar2;
DROP TABLE IF EXISTS type_nchar2;