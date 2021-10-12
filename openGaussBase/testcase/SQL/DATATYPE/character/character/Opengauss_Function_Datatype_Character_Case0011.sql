-- @testpoint: 插入正常值，字节长度为默认值
-- @modify at: 2020-11-05


drop table if exists test_character_11;
create table test_character_11 (name character);
insert into test_character_11 values ('a');
select * from test_character_11;
drop table test_character_11;