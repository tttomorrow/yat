-- @testpoint: 删除表数据后使用alter table语句修改列名，数据类型，无法转换的类型间合理报错
-- @modify at: 2020-11-23
--建表
drop table if exists temp_table_alter_015;
create global temporary table temp_table_alter_015(
c_id int,
c_real real,
c_char char(50) default null,
c_clob clob,
c_raw raw(20),
c_blob blob,
c_date date
)on commit preserve rows;
--插入数据
insert into temp_table_alter_015 select * from temp_table_alter_015;
--查询表
select * from temp_table_alter_015;
--清空数据
truncate table temp_table_alter_015;
--修改列名
alter table temp_table_alter_015  rename column c_real to c_2;
--修改数据类型real为varchar
alter table temp_table_alter_015 modify (c_2 varchar(200));
--修改数据类型raw为double
alter table temp_table_alter_015 modify (c_raw double precision);
--删表
drop table temp_table_alter_015;