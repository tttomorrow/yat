-- @testpoint: 插入正常值，设定字节长度为1
-- @modify at: 2020-11-05


drop table if exists test_character_04;
create table test_character_04 (name character(1));
insert into test_character_04 values ('a');
select * from test_character_04;
drop table test_character_04;