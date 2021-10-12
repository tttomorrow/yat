-- @testpoint: 表中插入数据，alter table为列添加check约束，插入数据违背该约束时合理报错
drop table if exists table_alter_016;
create table table_alter_016 (c1 int,ad VARCHAR(4000) NULL,ad1 VARCHAR(4000) NULL);
insert into table_alter_016(ad) values ('unconfirmed');

alter table table_alter_016 add constraint table_alter_016_check check(ad in ('confirmed','unconfirmed'));
alter table table_alter_016 modify ad not null;

SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'table_alter_016' and a.attrelid = c.oid and a.attnum>0;
insert into table_alter_016(ad) values ('confirmed');
insert into table_alter_016(ad) values (3);
alter table table_alter_016 drop constraint table_alter_016_check;
insert into table_alter_016(ad) values(1);
drop table if exists table_alter_016;