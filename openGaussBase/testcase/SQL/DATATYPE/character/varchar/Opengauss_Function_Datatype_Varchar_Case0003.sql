-- @testpoint: 字节长度设定为负数，合理报错
-- @modify at: 2020-11-17

drop table if exists test_varchar_03;
create table test_varchar_03 (name varchar(-1));
