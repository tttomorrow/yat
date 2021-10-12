-- @testpoint: 修改的列的数据类型范围不对，合理报错
drop table if exists test_modify cascade;
create table test_modify(
c_id int,
c_integer integer,
c_real real,
c_float float,
c_cdouble binary_double,
c_decimal decimal(38),
c_number number(38),
c_number1 number,
c_number2 number(20,10),
c_numeric numeric(38),
c_char char(50) default null,
c_varchar varchar(20),
c_varchar2 varchar2(4000),
c_clob clob,
c_raw raw(20),
c_blob blob,
c_date date,
c_timestamp timestamp
);
--查询字段信息
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_modify' and a.attrelid = c.oid and a.attnum>0;


alter table test_modify MODIFY (c_raw raw(0));

alter table test_modify MODIFY (c_char char(0));
alter table test_modify MODIFY (c_char char(-1));


alter table test_modify MODIFY (c_decimal decimal(-1));
alter table test_modify MODIFY (c_decimal decimal(0));
alter table test_modify MODIFY (c_decimal decimal(1000));
alter table test_modify MODIFY (c_decimal decimal(1001));

alter table test_modify MODIFY (c_number2 number(-1,0));
alter table test_modify MODIFY (c_number2 number(0,-1));
alter table test_modify MODIFY (c_number2 number(0,0));
alter table test_modify MODIFY (c_number2 number(1000,0));
alter table test_modify MODIFY (c_number2 number(0,1000));
alter table test_modify MODIFY (c_number2 number(1000,1000));
alter table test_modify MODIFY (c_number2 number(1000,1001));
alter table test_modify MODIFY (c_number2 number(1001,1000));

alter table test_modify MODIFY (c_numeric numeric(-1));
alter table test_modify MODIFY (c_numeric numeric(0));
alter table test_modify MODIFY (c_numeric numeric(1000));
alter table test_modify MODIFY (c_numeric numeric(1001));


--查询字段信息
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_modify' and a.attrelid = c.oid and a.attnum>0;
drop table if exists test_modify cascade;
