-- @testpoint: 插入其他类型

drop table if exists special_char_06;
CREATE  TABLE special_char_06 (id "char");
insert into special_char_06 values ('test');
insert into special_char_06 values (100.999);
insert into special_char_06 values (date'2020-02-02');
insert into special_char_06 values (TRUE);
insert into special_char_06 values (HEXTORAW('DEADBEEF'));
select * from special_char_06;
drop table if exists special_char_06;