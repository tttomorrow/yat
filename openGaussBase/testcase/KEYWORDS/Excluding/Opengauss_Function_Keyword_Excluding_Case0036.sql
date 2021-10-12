-- @testpoint: 创建表指定like选项，使用excluding关键字

drop table if exists test_1;
create table test_1 (id int not null,name char(20)not null);
drop table if exists test_2;
create table test_2(like test_1 excluding CONSTRAINTS);
select * from test_2;
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_2' and a.attrelid = c.oid and a.attnum>0;


insert into test_2 values (1,'abc'),(2,'bcd');
select * from test_2;
drop table if exists test_1;
drop table if exists test_2;