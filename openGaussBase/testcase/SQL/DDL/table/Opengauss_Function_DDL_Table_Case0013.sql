-- @testpoint: alter table修改列类型，列不存在时合理报错
DROP TABLE IF EXISTS table_alter_013;
create table table_alter_013(
c_id int, c_integer integer,
c_real real,c_float float, c_double binary_double,
c_decimal decimal(38), c_number number(38),c_number1 number,c_number2 number(20,10),c_numeric numeric(38),
c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
c_clob clob,
c_raw raw(20),c_blob blob,
c_date date,c_timestamp timestamp
);
create index table_alter_013_idx2 on table_alter_013(c_integer);
create index table_alter_013_idx3 on table_alter_013(c_varchar);
create index table_alter_013_idx4 on table_alter_013(c_char);
create index table_alter_013_idx5 on table_alter_013(c_timestamp);
create index table_alter_013_idx6 on table_alter_013(c_id,c_integer,c_number);
create index table_alter_013_idx7 on table_alter_013(c_id,c_varchar,c_char,c_timestamp);
alter table table_alter_013 add  CONSTRAINT table_alter_013_pk PRIMARY KEY (c_id);
alter table table_alter_013 MODIFY (c_id char(20));
alter table table_alter_013 MODIFY (c_varchar char(80),C_NUMBER1 CLOB);
alter table table_alter_013 MODIFY (c_id char(20));
alter table table_alter_013  alter c_char set default 50;
alter table table_alter_013 MODIFY (c_varchar char(80),C_NUMBER4 DATE);
insert into table_alter_013 values('1',0,3.14,1.0002,3.55555,5,7887.656,0,0.111111,3.1415926,'dghg','jjj','pokj99',
);
alter table table_alter_013 MODIFY (c_id int);
alter table table_alter_013 MODIFY (c_varchar float8,C_NUMBER1 date);
drop table table_alter_013;

