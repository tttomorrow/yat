-- @testpoint: 插入正常值，字节长度设定为0，合理报错
-- @modified at: 2020-11-16

drop table if exists test_nvarchar2_14;
create table test_nvarchar2_14 (name nvarchar2(0));
