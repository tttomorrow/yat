-- @testpoint: 建表添加参数on commit delete rows,修改表属性，无法隐式转换的类型，合理报错
--开启事务
start transaction;
--建表
drop table if exists temp_table_alter_016;
create global temporary table temp_table_alter_016(
c_id int,
c_real real,
c_char char(50) default null,
c_clob clob,
c_raw raw(20),
c_blob blob,
c_date date
)on commit delete rows;
--插入数据
insert into temp_table_alter_016 values(1,1.0002,'dghg','jjjsdfghjhjui','010111100','010101101',date_trunc('hour', timestamp  '2001-02-16 20:38:40'));
--查询表数据，存在
select * from temp_table_alter_016;
--提交事务
commit;
--查询表,无数据
select * from temp_table_alter_016;
--修改列名
alter table temp_table_alter_016  rename column c_real to c_2;
--修改real类型改为varchar
alter table temp_table_alter_016 modify (c_2 varchar(20));
--修改raw类型为float,报错
alter table temp_table_alter_016 modify (c_raw float8);
--删表
drop table temp_table_alter_016;