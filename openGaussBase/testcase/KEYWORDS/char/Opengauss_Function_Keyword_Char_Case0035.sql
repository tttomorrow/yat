-- @testpoint: 不带精度n，默认精度为1，插入精度为2的字符合理报错
drop table if exists char_type_t1;
CREATE TABLE char_type_t1(CT_COL1 CHAR);
insert into char_type_t1 (CT_COL1) values('he');
drop table if exists char_type_t1;