-- @testpoint: 在创建check约束之后，修改字段的约束，新插入数据违背约束时合理报错

--建表
drop table if exists t1 cascade;
create table t1 (c1 int,c2 VARCHAR(4000) NULL,ad VARCHAR(4000) NULL);

--查询字段类型
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 't1' and a.attrelid = c.oid and a.attnum>0;

--添加约束后修改字段信息：修改成功
alter table t1 add constraint cc check(ad in ('confirmed','unconfirmed'));
alter table t1 modify ad null;
alter table t1 modify ad not null;
alter table t1 modify ad int;

--查询字段类型
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 't1' and a.attrelid = c.oid and a.attnum>0;

--插入数据，不符合检查约束，报错
insert into t1(ad) values (3);
insert into t1(ad) values (null);
insert into t1(ad) values ('confirmed');


--drop检查约束
alter table t1 drop constraint cc;

--插入信息
insert into t1(ad) values(1);

SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 't1' and a.attrelid = c.oid and a.attnum>0;

drop table if exists t1 cascade;