-- @testpoint: 插入索引后，修改列
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

create index test_modify_idx1 on test_modify(c_id);
create index test_modify_idx2 on test_modify(c_integer);
create index test_modify_idx3 on test_modify(c_varchar);
create index test_modify_idx4 on test_modify(c_char);
create index test_modify_idx5 on test_modify(c_timestamp);
create index test_modify_idx6 on test_modify(c_id,c_integer,c_number);
create index test_modify_idx7 on test_modify(c_id,c_varchar,c_char,c_timestamp);
alter table test_modify MODIFY (c_varchar char(80),c_timestamp DATE);

SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_modify' and a.attrelid = c.oid and a.attnum>0;

drop table if exists test_modify cascade;
