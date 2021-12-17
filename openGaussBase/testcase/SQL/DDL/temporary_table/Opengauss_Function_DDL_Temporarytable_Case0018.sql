-- @testpoint: 删除表数据后使用alter table语句，无法隐式转换的类型，合理报错
--建表
drop table if exists temp_table_alter_018;
create global temporary table temp_table_alter_018(
c_id int,
c_real real,
c_char char(50) default null,
c_clob clob,
c_raw raw(20),
c_blob blob,
c_date date
)on commit preserve rows;
--插入数据
insert into temp_table_alter_018 values(1,1.0002,'dghg','jjjsdfghjhjui','010111100','010101101',date_trunc('hour', timestamp  '2001-02-16 20:38:40'));
insert into temp_table_alter_018 values(2,1.0002,'dghg','jjjsdfghjhjui','010111100','010101101',date_trunc('hour', timestamp  '2001-02-16 20:38:40'));
insert into temp_table_alter_018 select * from temp_table_alter_018;
insert into temp_table_alter_018 select * from temp_table_alter_018;
insert into temp_table_alter_018 select * from temp_table_alter_018;
insert into temp_table_alter_018 select * from temp_table_alter_018;
insert into temp_table_alter_018 select * from temp_table_alter_018;
insert into temp_table_alter_018 select * from temp_table_alter_018;
--清空表数据
truncate table temp_table_alter_018;
--修改列名
alter table temp_table_alter_018  rename column c_real to c_2;
--real改为varchar
alter table temp_table_alter_018 modify (c_2 varchar(20));
--raw改为double
alter table temp_table_alter_018 modify (c_raw float8);
--查询表
select count(*) from temp_table_alter_018;
--删表
drop table temp_table_alter_018;


