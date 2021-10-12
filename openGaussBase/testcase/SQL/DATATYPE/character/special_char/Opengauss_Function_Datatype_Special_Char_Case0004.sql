-- @testpoint: 创建表，将“char”数据类型转换至boolean、date，合理报错

drop table if exists special_char_04;
CREATE  TABLE special_char_04 (id "char");
insert into special_char_04 values ('a');
alter table special_char_04 alter column id TYPE BOOLEAN;

drop table if exists special_char_04;
CREATE  TABLE special_char_04 (id "char");
insert into special_char_04 values ('a');
alter table special_char_04 alter column id TYPE date;

drop table if exists special_char_04;