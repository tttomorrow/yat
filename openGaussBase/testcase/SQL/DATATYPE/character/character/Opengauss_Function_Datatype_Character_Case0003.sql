-- @testpoint: 字节长度设定为负数，合理报错
-- @modify at: 2020-11-05


drop table if exists test_character_03;
create table test_character_03 (name character(-1));

