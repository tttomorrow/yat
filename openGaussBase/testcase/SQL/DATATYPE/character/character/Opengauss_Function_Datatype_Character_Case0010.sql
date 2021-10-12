-- @testpoint: 插入值为中文，超出字节设定长度，合理报错
-- @modify at: 2020-11-05

drop table if exists test_character_09;
create table test_character_09 (name character(20));
insert into test_character_09 values ('高斯开源数据库');
drop table test_character_09;