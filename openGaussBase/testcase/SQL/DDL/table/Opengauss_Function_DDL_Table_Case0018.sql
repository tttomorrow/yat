-- @testpoint: delete 删除部分表数据后alter table

drop table if exists table_alter_018;
create table table_alter_018(
c_id int,
c_real real,
c_char char(50) default null,
c_clob clob,
c_blob blob,
c_date date
);

insert into table_alter_018 select * from table_alter_018;
insert into table_alter_018 select * from table_alter_018;
insert into table_alter_018 select * from table_alter_018;
insert into table_alter_018 select * from table_alter_018;
insert into table_alter_018 select * from table_alter_018;
insert into table_alter_018 select * from table_alter_018;
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'table_alter_018' and a.attrelid = c.oid and a.attnum>0;
delete from table_alter_018 where  c_id=1;
--rename
alter table table_alter_018  rename COLUMN c_real to c_2;
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'table_alter_018' and a.attrelid = c.oid and a.attnum>0;

--real改为varchar
alter table table_alter_018 MODIFY (c_2 varchar(20));
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'table_alter_018' and a.attrelid = c.oid and a.attnum>0;
drop table if exists table_alter_018;
