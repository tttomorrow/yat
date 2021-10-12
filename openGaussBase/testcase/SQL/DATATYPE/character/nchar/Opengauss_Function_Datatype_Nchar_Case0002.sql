-- @testpoint: 插入正常值

DROP TABLE IF EXISTS type_nchar_02;
CREATE TABLE type_nchar_02 (stringv nchar(20));
insert into type_nchar_02 values ('ou mygod');
select * from type_nchar_02;
DROP TABLE type_nchar_02;