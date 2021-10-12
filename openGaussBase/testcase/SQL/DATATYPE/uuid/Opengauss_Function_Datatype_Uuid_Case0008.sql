-- @testpoint: 插入非正常范围数据，合理报错

drop table if exists test_uuid_08;
create table test_uuid_08 (id uuid);
insert into test_uuid_08 values ('fffffffff-9c0b-4ef8-bb6d-6bb9bd380a11');
insert into test_uuid_08 values ('a0eebc99-fffff-4ef8-bb6d-6bb9bd380a11');
insert into test_uuid_08 values ('a0eebc99-9c0b-fffff-bb6d-6bb9bd380a11');
insert into test_uuid_08 values ('a0eebc99-9c0b-4ef8-fffff-6bb9bd380a11');
insert into test_uuid_08 values ('a0eebc99-9c0b-4ef8-bb6d-fffffffff');
drop table test_uuid_08;