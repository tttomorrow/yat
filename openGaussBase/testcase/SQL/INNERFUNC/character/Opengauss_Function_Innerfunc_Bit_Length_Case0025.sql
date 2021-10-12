-- @testpoint: 正常值插入CHARACTER VARYING(n)

DROP TABLE IF EXISTS type_nchar2;
CREATE TABLE type_nchar2 (stringv CHARACTER VARYING(100));
insert into type_nchar2 values ('ou mygod中>%');
select bit_length(stringv) from type_nchar2;
DROP TABLE IF EXISTS type_nchar2;