-- @testpoint: 插入超出范围值，字节长度设定为合理值，合理报错
-- @modified at:2020-11-16

drop table if exists test_nvarchar2_13;
create table test_nvarchar2_13 (name nvarchar2(20));
insert into test_nvarchar2_13 values ('aaaaaaaaaaaaaaaaaaaaa');
drop table if exists test_nvarchar2_13;