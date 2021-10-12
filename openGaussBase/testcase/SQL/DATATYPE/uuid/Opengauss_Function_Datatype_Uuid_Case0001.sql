-- @testpoint: 创建行存表，插入数据

drop table if exists test_uuid_01;
create table test_uuid_01 (id uuid) with(orientation=row, compression=no);
insert into test_uuid_01 values ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11');
insert into test_uuid_01 values ('A0EEBC99-9C0B-4EF8-BB6D-6BB9BD380A11');
select * from test_uuid_01;
drop table test_uuid_01;