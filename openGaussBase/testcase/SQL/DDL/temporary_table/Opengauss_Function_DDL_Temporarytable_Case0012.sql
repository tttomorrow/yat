-- @testpoint: 修改数据类型，修改不存在的列合理报错；修改的列类型与插入数据类型不符，合理报错
-- @modify at: 2020-11-23
--建表1
DROP TABLE IF EXISTS temp_table_alter_012;
create global TEMPORARY table temp_table_alter_012(
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
c_raw raw(20),c_blob blob,
c_date date,c_timestamp timestamp
)on commit preserve rows;
--创建索引
create index temp_table_alter_012_idx2 on temp_table_alter_012(c_integer);
create index temp_table_alter_012_idx3 on temp_table_alter_012(c_varchar);
create index temp_table_alter_012_idx4 on temp_table_alter_012(c_char);
create index temp_table_alter_012_idx5 on temp_table_alter_012(c_timestamp);
create index temp_table_alter_012_idx6 on temp_table_alter_012(c_id,c_integer,c_number);
create index temp_table_alter_012_idx7 on temp_table_alter_012(c_id,c_varchar,c_char,c_timestamp);
--创建约束
alter table temp_table_alter_012 add  CONSTRAINT temp_table_alter_012_pk PRIMARY KEY (c_id);
--建表2
DROP TABLE IF EXISTS temp_table_alter_012_bak;
create global TEMPORARY table temp_table_alter_012_bak(a char(20));
--修改数据类型
alter table temp_table_alter_012 MODIFY (c_id char(20));
alter table temp_table_alter_012 MODIFY (c_varchar char(80),C_NUMBER1 CLOB);
alter table temp_table_alter_012 MODIFY (c_id char(20));
alter table temp_table_alter_012  alter c_char set default 50;
--修改不存在的列，报错
alter table temp_table_alter_012 MODIFY (c_varchar char(80),C_NUMBER4 DATE);
--插入数据
insert into temp_table_alter_012 values('1',0,3.14,1.0002,3.55555,5,7887.656,0,0.111111,3.1415926,'dghg','jjj','pokj99',
--修改类型
alter table temp_table_alter_012 MODIFY (c_id int);
--修改类型，报错
alter table temp_table_alter_012 MODIFY (c_varchar float8,C_NUMBER1 date);
--删表
drop table temp_table_alter_012;
drop table temp_table_alter_012_bak;


