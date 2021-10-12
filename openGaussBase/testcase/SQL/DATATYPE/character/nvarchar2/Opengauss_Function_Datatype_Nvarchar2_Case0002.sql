-- @testpoint: 字节长度设定为负数，合理报错
-- @modified at: 2020-11-16

drop table if exists test_nvarchar2_02;
create table test_nvarchar2_02 (name nvarchar2(-1));
