-- @testpoint: 插入空值

drop table if exists test_uuid_06;
create table test_uuid_06 (id1 int,id2 uuid);
insert into test_uuid_06 values (1,null);
insert into test_uuid_06 values (2,'');
select * from test_uuid_06;
drop table test_uuid_06;