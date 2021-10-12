-- @testpoint: uuid数据类型转换至tinyint/date,合理报错

drop table if exists test_uuid_04;
create table test_uuid_04 (id uuid);
insert into test_uuid_04 values ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11');
--修改数据类型为tinyint
alter table test_uuid_04 alter column id type tinyint;
--修改数据类型为date
alter table test_uuid_04 alter column id type date;
--查看字段类型
select format_type(a.atttypid,a.atttypmod) as type from pg_class as c,pg_attribute as a where c.relname = 'test_uuid_04' and a.attrelid = c.oid and a.attnum>0;

drop table test_uuid_04;