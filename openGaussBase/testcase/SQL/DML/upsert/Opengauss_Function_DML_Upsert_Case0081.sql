--  @testpoint:创建表未指定主键约束，使用alter语句增加主键约束后使用insert..nothing语句
--预置条件enable_upsert_to_merge为off
drop table if exists test4;
--创建表未指定主键约束
create table test4 (id int ,name varchar(20) );
--给id列添加主键约束
ALTER TABLE test4 ADD CONSTRAINT id_key primary key (id);
--使用insert常规插入一条数据
insert into test4 values(5,'daliu');
select * from test4;
--使用insert..nothing语句,主键均不重复，新增两条数据(6,'lisa1'),(7,'lisa2')
insert into test4 values(6,'lisa1'),(7,'lisa2') on DUPLICATE key update nothing;
select * from test4;
--使用insert..nothing语句,主键重复,直接返回，故更新0条数据
insert into test4 values(5,'lisa1'),(7,'lisa2') on DUPLICATE key update nothing;
select * from test4;
--使用insert..nothing语句，第一条数据主键id重复，第二条数据主键不重复，故新增一条数据(9,'lisa2')
insert into test4 values(5,'lisa1'),(9,'lisa2') on DUPLICATE key update nothing;
select * from test4;
drop table test4;