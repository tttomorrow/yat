-- @testpoint: alter多次--同个命令执行多次
drop table if exists table_alter_020;
create table table_alter_020(
c_id int,
c_real real,
c_char char(50) default null,
c_clob clob,
c_raw raw(20),
c_blob blob,
c_date date
);
create index table_alter_020_idx1 on table_alter_020(c_id);
create index table_alter_020_idx2 on table_alter_020(c_raw);
--修改数据类型执行多次
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));

insert into table_alter_020 select * from table_alter_020;
insert into table_alter_020 select * from table_alter_020;
insert into table_alter_020 select * from table_alter_020;
insert into table_alter_020 select * from table_alter_020;
insert into table_alter_020 select * from table_alter_020;
insert into table_alter_020 select * from table_alter_020;
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'table_alter_020' and a.attrelid = c.oid and a.attnum>0;
--删除索引
drop index table_alter_020_idx2;
--rename
alter table table_alter_020  rename COLUMN c_real to c_2;
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'table_alter_020' and a.attrelid = c.oid and a.attnum>0;
--real改为varchar
alter table table_alter_020 MODIFY (c_2 varchar(20));
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'table_alter_020' and a.attrelid = c.oid and a.attnum>0;
--修改数据类型执行多次
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));
alter table table_alter_020 MODIFY (c_raw varchar(10));alter table table_alter_020 MODIFY (c_raw raw(20));



SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'table_alter_020' and a.attrelid = c.oid and a.attnum>0;
drop table if exists table_alter_020;