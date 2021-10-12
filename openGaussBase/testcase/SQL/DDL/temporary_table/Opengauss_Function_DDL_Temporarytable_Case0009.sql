-- @testpoint: 无法进行隐式转换的类型间互相修改类型，合理报错
-- @modify at: 2020-11-23
--创建全局临时表
drop table if exists temp_table_alter_009;
create global temporary table temp_table_alter_009(
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
--修改类型
alter table temp_table_alter_009 modify(c_integer char(60));
alter table temp_table_alter_009 modify(c_float int);
alter table temp_table_alter_009 modify(c_number char(60));
--修改日期型为real型，合理报错
alter table temp_table_alter_009 modify(c_date real);
--插入数据
insert into temp_table_alter_009 values(1,0,3.14,1.0002,3.55555,5,7887.656,0,0.111111,3.1415926,'dghg','jjj','pokj99',
--查询表
select * from temp_table_alter_009;
--删表
drop table temp_table_alter_009;
