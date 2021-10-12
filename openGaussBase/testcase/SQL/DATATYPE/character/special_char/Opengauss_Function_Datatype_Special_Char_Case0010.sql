-- @testpoint: 创建行存本地临时表，字段类型为“char”


drop table if exists special_char_10;
CREATE TEMPORARY TABLE special_char_10 (id "char") WITH (orientation=row, compression=no);
insert into special_char_10 values ('t');
select * from special_char_10;
drop table special_char_10;