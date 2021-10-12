-- @testpoint: 字节长度为负数测试，合理报错
-- @modify at: 2020-11-05

drop table if exists test_char_02;
create table test_char_02 (name char(-1));
