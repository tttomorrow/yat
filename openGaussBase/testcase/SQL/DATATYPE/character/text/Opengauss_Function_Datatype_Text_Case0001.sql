-- @testpoint: 创建表，设定字节长度为0，合理报错
-- @modified at: 2020-11-16

drop table if exists test_text_01;
create table test_text_01(c_clob text(0));
