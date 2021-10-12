-- @testpoint: 指定网络地址输入为空

drop table if exists test_inet_03;
create table test_inet_03(id int,type inet);
insert into test_inet_03 values(1,null);
insert into test_inet_03 values(2,'');
select * from test_inet_03;
drop table test_inet_03;
