-- @testpoint: 插入正常MAC类型值

drop table if exists test_macaddr_01;
create table test_macaddr_01(type macaddr);
insert into test_macaddr_01 values('08:00:2b:01:02:03');
insert into test_macaddr_01 values('08-00-2b-01-02-03');
insert into test_macaddr_01 values('08002b:010203');
insert into test_macaddr_01 values('0800.2b01.0203');
insert into test_macaddr_01 values('08002b010203');
select * from test_macaddr_01;
drop table test_macaddr_01;
