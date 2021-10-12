-- @testpoint: 创建临时表行存表，插入数据

drop table if exists test_uuid_12;
create temporary table test_uuid_12 (id uuid) with(orientation=row, compression=no);
insert into test_uuid_12 values ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11');
select * from test_uuid_12;
drop table test_uuid_12;