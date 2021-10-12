-- @testpoint: 插入非法空值，合理报错

drop table if exists test_uuid_05;
create table test_uuid_05 (c1 int,c2 uuid);
insert into test_uuid_05 values (1,' ');
drop table test_uuid_05;