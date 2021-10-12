-- @testpoint: 修改表数据，同一个命令执行多次
-- @modify at: 2020-11-23
--建表
drop table if exists temp_table_alter_019;
create global temporary table temp_table_alter_019(
c_id int,
c_real real,
c_char char(50) default null,
c_clob clob,
c_raw raw(20),
c_blob blob,
c_date date
)on commit preserve rows;
--修改数据类型执行多次
alter table temp_table_alter_019 modify (c_raw varchar(200));
alter table temp_table_alter_019 modify (c_raw raw(20));
alter table temp_table_alter_019 modify (c_raw varchar(200));
alter table temp_table_alter_019 modify (c_raw raw(20));
--插入数据
insert into temp_table_alter_019 select * from temp_table_alter_019;
insert into temp_table_alter_019 select * from temp_table_alter_019;
insert into temp_table_alter_019 select * from temp_table_alter_019;
insert into temp_table_alter_019 select * from temp_table_alter_019;
insert into temp_table_alter_019 select * from temp_table_alter_019;
insert into temp_table_alter_019 select * from temp_table_alter_019;
--查询
select count(*) from temp_table_alter_019;
--rename
alter table temp_table_alter_019  rename column c_real to c_2;
--real改为varchar
alter table temp_table_alter_019 modify (c_2 varchar(20));
--修改数据类型执行多次
alter table temp_table_alter_019 modify (c_raw varchar(200));
alter table temp_table_alter_019 modify (c_raw raw(20));
alter table temp_table_alter_019 modify (c_raw varchar(200));
alter table temp_table_alter_019 modify (c_raw raw(20));
--删表
drop table temp_table_alter_019 cascade;

