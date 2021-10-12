-- @testpoint: 指定网络地址为0

drop table if exists test_cidr_04;
create table test_cidr_04(id int,type cidr);
insert into test_cidr_04 values(1,'0');
insert into test_cidr_04 values(2,'0');
insert into test_cidr_04 values(3,'0');
select * from test_cidr_04;
drop table test_cidr_04;