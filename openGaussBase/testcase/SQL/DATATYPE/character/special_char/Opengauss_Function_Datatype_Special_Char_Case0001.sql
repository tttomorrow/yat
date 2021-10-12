-- @testpoint: 创建行存表，插入数据

drop table if exists special_char_01;
CREATE  TABLE special_char_01 (id "char") WITH (orientation=row, compression=no);
insert into special_char_01 values ('t');
select * from special_char_01;
drop table special_char_01;