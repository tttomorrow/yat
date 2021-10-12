-- @testpoint: 正常值插入VARCHAR

DROP TABLE IF EXISTS type_nchar2;
CREATE TABLE type_nchar2 (stringv  VARCHAR(5));
insert into type_nchar2 values ('ou mygod'::varchar(5));
select bit_length(stringv) from type_nchar2;
DROP TABLE IF EXISTS type_nchar2;