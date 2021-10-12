-- @testpoint: 创建列存表，插入数据


drop table if exists special_char_02;
CREATE  TABLE special_char_02 (id "char") WITH (orientation=COLUMN, compression=no);
insert into special_char_02 values ('t');
select * from special_char_02;
drop table if exists special_char_02;