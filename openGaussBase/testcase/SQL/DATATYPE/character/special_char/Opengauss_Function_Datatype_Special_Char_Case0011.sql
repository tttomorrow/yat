-- @testpoint: 创建列存本地临时表，字段类型为“char”


drop table if exists special_char_11;
CREATE TEMPORARY TABLE special_char_11 (id "char") WITH (orientation=COLUMN, compression=no);
insert into special_char_11 values ('t');
select * from special_char_11;
drop table if exists special_char_11;