-- @testpoint: 指定正常网络地址输入值

drop table if exists test_cidr_01;
create table test_cidr_01(type cidr);
insert into test_cidr_01 values('192.168.100.128/25');
insert into test_cidr_01 values('192.168.31/24');
insert into test_cidr_01 values('10.1');
insert into test_cidr_01 values('192.168');
insert into test_cidr_01 values('0.0.0.0/24');
select * from test_cidr_01;
drop table test_cidr_01;
