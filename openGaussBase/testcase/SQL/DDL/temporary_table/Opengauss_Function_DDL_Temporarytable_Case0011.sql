-- @testpoint: 同时新增多列，数据类型包含blob、clob类型
-- @modify at: 2020-11-23
--建表
drop table if exists temp_table_alter_011;
create global temporary table temp_table_alter_011(c_id int, c_integer integer,c_real real,c_float float, c_double binary_double
)on commit preserve rows;
--增加多列
alter table temp_table_alter_011 add(c_decimal decimal(38), c_number number(38),c_number1 number,c_number2 number(20,10),c_numeric numeric(38),
c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),c_clob clob);
alter table temp_table_alter_011 add(c_raw raw(20),c_blob blob,c_date date,c_timestamp timestamp);
--插入数据
insert into temp_table_alter_011 values(1,0,3.14,1.0002,3.55555,5,7887.656,0,0.111111,3.1415926,'dghg','jjj','pokj99',
'ywgdghghhgghe',hextoraw('101a1101'),'010101101',date_trunc('hour', timestamp  '2001-02-16 20:38:40'),
to_timestamp('2019-01-03 14:58:54.000000','yyyy-mm-dd hh24:mi:ss.ffffff'));
insert into temp_table_alter_011 select * from temp_table_alter_011;
insert into temp_table_alter_011 select * from temp_table_alter_011;
insert into temp_table_alter_011 select * from temp_table_alter_011;
analyze temp_table_alter_011;
--修改列名
alter table temp_table_alter_011  rename column c_varchar to c_1;
alter table temp_table_alter_011  rename column c_real to c_2;
alter table temp_table_alter_011  rename column c_clob to c_3;
--查询表
select * from temp_table_alter_011;
--删除表数据并删除多列
delete  temp_table_alter_011;
alter table temp_table_alter_011 drop c_1;
alter table temp_table_alter_011 drop c_decimal;
alter table temp_table_alter_011 drop  c_date;
--删除表
drop table temp_table_alter_011;


