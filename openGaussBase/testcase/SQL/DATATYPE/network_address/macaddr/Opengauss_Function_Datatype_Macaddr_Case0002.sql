-- @testpoint: 插入无效MAC类型值，合理报错

drop table if exists test_macaddr_02;
create table test_macaddr_02(type macaddr);
insert into test_macaddr_02 values('08:00:2b:01:02:0W');
insert into test_macaddr_02 values('08-00-2b-01-02-0@');
insert into test_macaddr_02 values('08002b:01020#');
insert into test_macaddr_02 values('08002b-010W03');
insert into test_macaddr_02 values('0800.2bW1.0203');
drop table test_macaddr_02;
