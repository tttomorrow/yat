-- @testpoint: 指定网络地址类型输入值为空

drop table if exists test_cidr_03;
create table test_cidr_03(id int,type cidr);
insert into test_cidr_03 values(1,null);
insert into test_cidr_03 values(2,'');
select * from test_cidr_03;
drop table test_cidr_03;