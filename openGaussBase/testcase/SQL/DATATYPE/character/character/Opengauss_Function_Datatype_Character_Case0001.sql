-- @testpoint: 字节长度设定为0，合理报错
-- @modify at: 2020-11-05

--character类型字节设置为0，创建表失败，至少为1
drop table if exists test_character_01;
create table test_character_01 (name character(0));
