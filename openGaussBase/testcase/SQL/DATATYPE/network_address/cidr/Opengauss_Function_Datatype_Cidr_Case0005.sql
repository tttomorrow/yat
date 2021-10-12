-- @testpoint: 16进制IPV4网络地址

drop table if exists test_cidr_05;
create table test_cidr_05(id int,type cidr);
insert into test_cidr_05 values(1,'ABCD:EF01:2345:6789:ABCD:EF01:2345:6789');
insert into test_cidr_05 values(2,'2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128');
select * from test_cidr_05;
drop table test_cidr_05;