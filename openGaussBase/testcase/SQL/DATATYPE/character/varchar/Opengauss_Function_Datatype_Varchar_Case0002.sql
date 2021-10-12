-- @testpoint: 字节长度设定为0，合理报错
-- @modify at: 2020-11-17

drop table if exists test_varchar_02;
create table test_varchar_02 (name varchar(0));

