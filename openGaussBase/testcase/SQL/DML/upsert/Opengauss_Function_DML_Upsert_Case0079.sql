--  @testpoint:创建表未指定主键约束，使用alter语句增加主键约束后使用insert..update语句
--预置条件enable_upsert_to_merge为off
drop table if exists test2;
--创建表未指定主键约束
create table test2 (id int ,name varchar(20) );
--给id列添加主键约束
ALTER TABLE test2 ADD CONSTRAINT id_key primary key (id);
--使用insert常规插入一条数据
insert into test2 values(5,'daliu');
select * from test2;
--使用insert..update语句插入一条数据，主键id重复，故更新name字段的值，原数据(5,'daliu')更改为(5,'lisa')
insert into test2 values(5,'lisa') ON DUPLICATE KEY UPDATE  name='lisa';
select * from test2;
--使用insert..update语句插入一条数据，主键id不重复，故新增一条数据(6,'lisa1')
insert into test2 values(6,'lisa1') ON DUPLICATE KEY UPDATE name='lisa1';
select * from test2;
drop table test2;