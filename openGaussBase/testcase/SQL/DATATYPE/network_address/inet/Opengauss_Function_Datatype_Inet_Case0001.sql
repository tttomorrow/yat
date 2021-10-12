-- @testpoint: 指定正常网络地址类型输入值

drop table if exists test_inet_01;
create table test_inet_01(type inet);
insert into test_inet_01 values('192.168.31.32/24');
insert into test_inet_01 values('192.168.31/24');
insert into test_inet_01 values('0.0.0.0/24');
select * from test_inet_01;
drop table test_inet_01;