-- @testpoint: 插入MAC地址0值，合理报错

drop table if exists test_macaddr_04;
create table test_macaddr_04(id int,type macaddr);
insert into test_macaddr_04 values(1,0);
insert into test_macaddr_04 values(2,0);
insert into test_macaddr_04 values(3,0);
drop table test_macaddr_04;
