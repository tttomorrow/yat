-- @testpoint: 修改列的约束为主键约束
-- @modify at: 2020-11-23
--创建全局临时表
drop table if exists temp_table_alter_006;
create global temporary table temp_table_alter_006(
c_id int,
c_integer integer,
c_real real,
c_float float,
c_double binary_double,
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
--修改约束
alter table temp_table_alter_006 add constraint  temp_table_alter_006_key primary key (c_id);
--从系统表查询表信息
select col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
from pg_class as c,pg_attribute as a where c.relname = 'temp_table_alter_006' and a.attrelid = c.oid and a.attnum>0;
--删表
drop table temp_table_alter_006;