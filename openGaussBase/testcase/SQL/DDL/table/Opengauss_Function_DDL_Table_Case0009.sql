-- @testpoint: 表中插入数据，对char、varchar类型可以相互进行MODIFY 操作,超长时合理报错
drop table if exists table_alter_009;
create table table_alter_009(a CHAR,c VARCHAR(10));
alter table table_alter_009 modify(a VARCHAR(60));
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'table_alter_009' and a.attrelid = c.oid and a.attnum>0;
insert into table_alter_009 values('dddddhdfghjkl5455221%^%^&*&&*edrtfyuio',90);
insert into table_alter_009 select * from table_alter_009;
insert into table_alter_009 select * from table_alter_009;
alter table table_alter_009 modify(a char(60));
alter table table_alter_009 modify(a VARCHAR(30));
alter table table_alter_009 modify(a VARCHAR(100));
alter table table_alter_009 modify(a CHAR(300));
alter table table_alter_009 modify(a VARCHAR(1000));
alter table table_alter_009 modify(a VARCHAR2(1000));
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'table_alter_009' and a.attrelid = c.oid and a.attnum>0;
drop table if exists table_alter_009;