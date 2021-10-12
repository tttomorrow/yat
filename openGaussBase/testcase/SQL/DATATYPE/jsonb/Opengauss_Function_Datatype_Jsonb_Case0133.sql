-- @testpoint: 创建表，并增加jsonb类型的列

--创建表
drop table if exists tab133;
create table tab133(c_id int, c_integer integer,c_real real,c_float float,
c_double binary_double,c_decimal decimal(38), c_number number(38),c_number1 number,
c_number2 number(20,10),c_numeric numeric(38),c_char char(50) default null, c_varchar varchar(20),
c_varchar2 varchar2(40),c_clob clob,c_raw raw(20),c_blob blob,c_date date,c_timestamp timestamp
);
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'tab133' and a.attrelid = c.oid and a.attnum>0;

--增加列
alter table tab133 add(c_add jsonb);
insert into tab133 values(1,0,3.14,1.0002,3.55555,5,7887.656,0,0.111111,3.1415926,'dghg','jjj','pokj99',
to_timestamp('2019-01-03 14:58:54.000000','YYYY-MM-DD HH24:MI:SS.FFFFFF'),'"add"');
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'tab133' and a.attrelid = c.oid and a.attnum>0;

--删除新增加的列
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'tab133' and a.attrelid = c.oid and a.attnum>0;
alter table tab133 drop c_add;

--清理数据
drop table if exists tab133 cascade;