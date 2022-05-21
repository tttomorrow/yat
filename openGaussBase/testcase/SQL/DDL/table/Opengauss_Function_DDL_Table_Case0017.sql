-- @testpoint: 删除表数据后alter table修改列类型

drop table if exists table_alter_017;
create table table_alter_017(
c_id int,
c_real real,
c_char char(50) default null,
c_clob clob,

c_blob blob,
c_date date
);
insert into table_alter_017 values(1,1.0002,'dghg','jjjsdfghjhjui','010101101',date_trunc('hour', timestamp  '2001-02-16 20:38:40'));
delete from table_alter_017;
--rename
alter table table_alter_017  rename COLUMN c_real to c_2;
--real改为varchar
alter table table_alter_017 MODIFY (c_2 varchar(20));
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'table_alter_017' and a.attrelid = c.oid and a.attnum>0;
drop table if exists table_alter_017;