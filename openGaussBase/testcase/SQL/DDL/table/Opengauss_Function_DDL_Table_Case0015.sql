-- @testpoint: alter table对表进行多种类型的操作

drop table if exists temp_table_alter_015;
create table temp_table_alter_015(
c_id int,
c_real real,
c_char char(50) default null,
c_clob clob,
c_raw raw(20),
c_blob blob,
c_date date
);
--创建索引
create index temp_table_alter_015_idx1 on temp_table_alter_015(c_id);
create index temp_table_alter_015_idx2 on temp_table_alter_015(c_raw);
insert into temp_table_alter_015 select * from temp_table_alter_015;
insert into temp_table_alter_015 select * from temp_table_alter_015;
insert into temp_table_alter_015 select * from temp_table_alter_015;
insert into temp_table_alter_015 select * from temp_table_alter_015;
insert into temp_table_alter_015 select * from temp_table_alter_015;
insert into temp_table_alter_015 select * from temp_table_alter_015;
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'temp_table_alter_015' and a.attrelid = c.oid and a.attnum>0;
--rename
alter table temp_table_alter_015  rename COLUMN c_real to c_2;
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'temp_table_alter_015' and a.attrelid = c.oid and a.attnum>0;
--real改为varchar
alter table temp_table_alter_015 MODIFY (c_2 varchar(20));
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'temp_table_alter_015' and a.attrelid = c.oid and a.attnum>0;
--delete 删除表
delete from temp_table_alter_015;
--rename
alter table temp_table_alter_015  rename COLUMN c_2 to c_real;
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'temp_table_alter_015' and a.attrelid = c.oid and a.attnum>0;
--real改为varchar
alter table temp_table_alter_015 MODIFY (c_real varchar(20));
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'temp_table_alter_015' and a.attrelid = c.oid and a.attnum>0;

drop table if exists temp_table_alter_015;