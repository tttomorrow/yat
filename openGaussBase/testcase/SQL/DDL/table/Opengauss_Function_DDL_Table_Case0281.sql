-- @testpoint: 列存修改字段类型，为raw、blob时合理报错
drop table if exists test_modify;

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
c_date date,
c_timestamp timestamp
) with (ORIENTATION = COLUMN);

--ADD [ COLUMN ] column_name data_type [ compress_mode ] [ COLLATE collation ] [ column_constraint [ ... ] ]
--| MODIFY column_name data_type
--| MODIFY column_name [ CONSTRAINT constraint_name ] NOT NULL [ ENABLE ]
--| MODIFY column_name [ CONSTRAINT constraint_name ] NULL
--修改字段类型
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_modify' and a.attrelid = c.oid and a.attnum>0;


alter table test_modify modify (c_id varchar,c_integer varchar(20),c_real varchar);
alter table test_modify modify (c_float varchar,c_integer varchar(20),c_numeric varchar);
alter table test_modify modify (c_id varchar,c_cdouble varchar(20),c_decimal varchar);
alter table test_modify modify (c_number varchar,c_number1 varchar(20),c_number2 varchar);
alter table test_modify modify c_char int;
alter table test_modify modify (c_id clob,c_varchar clob,c_float clob);
alter table test_modify modify (c_id ,c_integer varchar(20),c_real varchar);
alter table test_modify modify (c_id varchar,c_integer varchar(20),c_real blob);
alter table test_modify modify (c_id varchar,c_integer varchar(20),c_real raw);


SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_modify' and a.attrelid = c.oid and a.attnum>0;

drop table if exists test_modify;
