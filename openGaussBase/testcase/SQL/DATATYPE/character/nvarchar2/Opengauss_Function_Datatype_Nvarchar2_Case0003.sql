-- @testpoint: 插入正常值，字节长度设定为1

drop table if exists test_nvarchar2_03;
create table test_nvarchar2_03 (name nvarchar2(1));
insert into test_nvarchar2_03 values ('a');
select * from test_nvarchar2_03;
drop table test_nvarchar2_03;