-- @testpoint: 指定错误网络地址输入值，合理报错

drop table if exists test_inet_02;
create table test_inet_02(type inet);
insert into test_inet_02 values('528.23.10.100/24');
insert into test_inet_02 values('192.623.10.100/24');
insert into test_inet_02 values('192.168.300.100/24');
drop table test_inet_02;
