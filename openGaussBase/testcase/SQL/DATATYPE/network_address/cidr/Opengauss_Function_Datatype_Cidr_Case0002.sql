-- @testpoint: 指定错误网络地址类型输入值，合理报错

drop table if exists test_cidr_02;
create table test_cidr_02(type cidr);
insert into test_cidr_02 values('528.23.10.100/24');
insert into test_cidr_02 values('192.623.10.100/24');
insert into test_cidr_02 values('192.168.300.100/24');
insert into test_cidr_02 values('192.168.32.623/24');
insert into test_cidr_02 values('192.168/322');
drop table test_cidr_02;
