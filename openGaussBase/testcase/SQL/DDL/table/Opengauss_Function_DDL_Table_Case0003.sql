-- @testpoint: 修改多列中包含不存在的列,合理报错

drop table if exists table_alter_003;
create table table_alter_003(
c_id int, c_integer integer,
c_real real,c_float float, c_double binary_double,
c_decimal decimal(38), c_number number(38),c_number1 number,c_number2 number(20,10),c_numeric numeric(38),
c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
c_clob clob,
c_raw raw(20),c_blob blob,
c_date date,c_timestamp timestamp
);
alter table table_alter_003 MODIFY (c_varchar char(80),C_NUMBER4 DATE);

SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'table_alter_003' and a.attrelid = c.oid and a.attnum>0;
drop table if exists table_alter_003;