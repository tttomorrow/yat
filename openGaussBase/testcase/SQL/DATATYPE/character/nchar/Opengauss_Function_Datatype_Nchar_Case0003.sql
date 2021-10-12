-- @testpoint: 字节长度设定为负数，合理报错
-- @modified at: 2020-11-16

drop table if exists test_nchar_03;
create table test_nchar_03 (name nchar(-1));
