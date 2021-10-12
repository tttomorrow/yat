--  @testpoint:创建表时加命名constraint定义主键约束，使用insert..update语句插入一条数据
--预置条件enable_upsert_to_merge为off
drop table if exists test1;
create table test1 (id int constraint idx_t_id primary key,name varchar(20) constraint cst_name not null);
--使用insert常规插入一条数据
insert into test1 values(1,'rudy');
select * from test1;
--使用insert..update语句，合理报错，没有该语法
insert into test1 values(1,'lisa')  ON CONSTRAINT idx_t_id  UPDATE  name='lisa';
select * from test1;
drop table test1;

