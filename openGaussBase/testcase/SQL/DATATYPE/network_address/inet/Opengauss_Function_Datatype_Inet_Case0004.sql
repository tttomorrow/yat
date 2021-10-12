-- @testpoint: 指定网络地址为0，合理报错

drop table if exists test_inet_04;
create table test_inet_04(id int,type inet);
insert into test_inet_04 values(1,0);
insert into test_inet_04 values(2,0);
select * from test_inet_04;
drop table test_inet_04;
