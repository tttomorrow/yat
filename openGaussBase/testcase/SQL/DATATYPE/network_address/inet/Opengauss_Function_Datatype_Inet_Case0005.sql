-- @testpoint: 16进制IPV6网络地址,合理报错

drop table if exists test_inet_05;
create table test_inet_05(id int,type inet);
insert into test_inet_05 values('2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128');
insert into test_inet_05 values('ABCD:EF01:2345:6789:ABCD:EF01:2345:6789');
select * from test_inet_05;
drop table test_inet_05;
