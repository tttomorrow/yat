-- @testpoint: 修改所有列的数据类型为 blob，合理报错
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

alter table test_modify MODIFY (C_ID BLOB,C_INTEGER BLOB,C_REAL BLOB,C_FLOAT BLOB,C_CDOUBLE BLOB,C_DECIMAL BLOB,C_NUMBER BLOB,C_NUMBER1 BLOB,C_NUMBER2 BLOB,C_NUMERIC BLOB,C_CHAR BLOB,C_VARCHAR BLOB,C_VARCHAR2 BLOB,C_RAW BLOB,C_DATE BLOB,C_TIMESTAMP BLOB);

--查询字段信息
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_modify' and a.attrelid = c.oid and a.attnum>0;


drop table if exists test_modify cascade;
