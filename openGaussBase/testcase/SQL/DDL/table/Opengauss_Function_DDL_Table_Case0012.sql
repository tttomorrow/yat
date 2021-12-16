-- @testpoint: alter table在插入数据前后进行添加删除多个列，重命名表后查询原表不存在合理报错

drop table if exists table_alter_012;
create table table_alter_012(c_id int, c_integer integer,c_real real,c_float float, c_double binary_double
);
--增加多列
alter table table_alter_012 add(c_decimal decimal(38), c_number number(38),c_number1 number,c_number2 number(20,10),c_numeric numeric(38),
c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),c_clob clob);
alter table table_alter_012 add(c_raw raw(20),c_blob blob,c_date date,c_timestamp timestamp);
--插入数据
insert into table_alter_012 values(1,0,3.14,1.0002,3.55555,5,7887.656,0,0.111111,3.1415926,'dghg','jjj','pokj99',
'ywgdghghhgghe',hextoraw('101A1101'),'010101101',date_trunc('hour', timestamp  '2001-02-16 20:38:40'),to_timestamp('2019-01-03 14:58:54.000000','YYYY-MM-DD HH24:MI:SS.FFFFFF')
);
insert into table_alter_012 select * from table_alter_012;
insert into table_alter_012 select * from table_alter_012;
insert into table_alter_012 select * from table_alter_012;
analyze table_alter_012;
--修改列
alter table table_alter_012  rename COLUMN c_varchar to c_1;
alter table table_alter_012  rename COLUMN c_real to c_2;
alter table table_alter_012  rename COLUMN c_clob to c_3;
--删除多列
delete  table_alter_012;
alter table table_alter_012 drop c_1;
alter table table_alter_012 drop c_decimal;
alter table table_alter_012 drop  c_date;
--删除表
drop table table_alter_012;
create table table_alter_012(c_id int, c_integer integer,c_real real,c_float float, c_double binary_double
);
--增加多列
alter table table_alter_012 add(c_decimal decimal(38), c_number number(38),c_number1 number,c_number2 number(20,10),c_numeric numeric(38),
c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),c_clob clob);
alter table table_alter_012 add(c_raw raw(20),c_blob blob,c_date date,c_timestamp timestamp);
--插入数据
insert into table_alter_012 values(1,0,3.14,1.0002,3.55555,5,7887.656,0,0.111111,3.1415926,'dghg','jjj','pokj99',
'ywgdghghhgghe',hextoraw('101A1101'),'010101101',date_trunc('hour', timestamp  '2001-02-16 20:38:40'),to_timestamp('2019-01-03 14:58:54.000000','YYYY-MM-DD HH24:MI:SS.FFFFFF')
);
insert into table_alter_012 select * from table_alter_012;
insert into table_alter_012 select * from table_alter_012;
insert into table_alter_012 select * from table_alter_012;
insert into table_alter_012 select * from table_alter_012;
insert into table_alter_012 select * from table_alter_012;
insert into table_alter_012 select * from table_alter_012;
insert into table_alter_012 select * from table_alter_012;
insert into table_alter_012 select * from table_alter_012;
insert into table_alter_012 select * from table_alter_012;
insert into table_alter_012 select * from table_alter_012;
insert into table_alter_012 select * from table_alter_012;
insert into table_alter_012 select * from table_alter_012;
analyze table_alter_012;
alter table table_alter_012 rename to table_alter_rename_012;
select count(*) from table_alter_012;
select count(*) from table_alter_rename_012;
drop table if exists table_alter_rename_012;


