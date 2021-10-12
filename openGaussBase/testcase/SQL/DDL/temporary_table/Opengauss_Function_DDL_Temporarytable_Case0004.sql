-- @testpoint: 修改表中raw数据类型
-- @modify at: 2020-11-23
--创建全局临时表
drop table if exists temp_table_alter_004;
create global temporary table temp_table_alter_004(
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
--修改
alter table temp_table_alter_004 modify (c_raw raw(0));
alter table temp_table_alter_004 modify (c_raw raw);
--插入数据，成功（raw类型无长度限制）
insert into temp_table_alter_004(c_double,c_raw) values(10.258,hextoraw('deadbeef'));
--从系统表查询表信息
select col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
from pg_class as c,pg_attribute as a where c.relname = 'temp_table_alter_004' and a.attrelid = c.oid and a.attnum>0;
--删表
drop table if exists temp_table_alter_004;