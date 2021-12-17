-- @testpoint: 表中插入数据前后，执行列的添加、删除操作
--建表
drop table if exists temp_table_alter_010;
create global temporary table temp_table_alter_010(
c_id int,
c_integer integer,
c_real real,
c_float float,
c_double binary_double,
c_decimal decimal(38),
c_number number(38),c_number1 number,
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
)on commit preserve rows;
--增加列
alter table temp_table_alter_010 add(c_1 int);
alter table temp_table_alter_010 add(c_2 blob default '0101010101111100001110');
alter table temp_table_alter_010 add(c_3 varchar(200));
alter table temp_table_alter_010 add(c_4 clob);
--查询表
select count(*) from temp_table_alter_010;
--删除新增加的列
alter table temp_table_alter_010 drop c_1;
alter table temp_table_alter_010 drop c_2;
alter table temp_table_alter_010 drop c_3;
--查询表
select * from temp_table_alter_010;
--插入数据
insert into temp_table_alter_010 values(1,0,3.14,1.0002,3.55555,5,7887.656,0,0.111111,3.1415926,'dghg','jjj','pokj99','
ywgdghghhgghe',hextoraw('101a1101'),'010101101',date_trunc('hour', timestamp  '2001-02-16 20:38:40'),
to_timestamp('2019-01-03 14:58:54.000000','yyyy-mm-dd hh24:mi:ss.ffffff'),'汉字的环境ihhivhkhv&*&%^&^555');
insert into temp_table_alter_010 select * from temp_table_alter_010;
insert into temp_table_alter_010 select * from temp_table_alter_010;
insert into temp_table_alter_010 select * from temp_table_alter_010;
analyze  temp_table_alter_010;
--查询表
select count(*) from temp_table_alter_010;
--删表
drop table temp_table_alter_010;
