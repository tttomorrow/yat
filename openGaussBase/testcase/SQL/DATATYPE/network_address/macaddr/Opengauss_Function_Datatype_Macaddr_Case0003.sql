-- @testpoint: 插入空值MAC类型

drop table if exists test_macaddr_03;
create table test_macaddr_03(id int,type macaddr);
insert into test_macaddr_03 values(1,'');
insert into test_macaddr_03 values(2,null);
select * from test_macaddr_03;
drop table test_macaddr_03;
