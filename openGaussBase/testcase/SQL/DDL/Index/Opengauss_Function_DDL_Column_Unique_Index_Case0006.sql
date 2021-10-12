-- @testpoint: 不同类型列存表，建表时指定主键、唯一约束，部分测试点合理报错

--创建普通列存表，单字段指定主键、唯一约束
drop table if exists columns_tab06;
create table columns_tab06(id1 int primary key,id2 int unique) with(orientation=column);

--创建列存本地临时表，单字段指定主键、唯一约束
drop table if exists columns_local_tab06;
create local temp table columns_local_tab06(id1 int primary key,id2 int unique) with(orientation=column);

--创建范围分区列存表，单字段指定主键、唯一约束
drop table if exists columns_part_tab06;
create table columns_part_tab06(id int primary key,name varchar) with(orientation=column)
partition by range(id)
(partition part_1 values less than(1000),
 partition part_2 values less than(2000),
 partition part_3 values less than(maxvalue));

--创建普通列存表，多字段指定主键、唯一键约束,合理报错
drop table if exists columnd_tab06;
create table columnd_tab06(id1 int primary key,id2 int primary key,name1 varchar unique,name2 char unique) with(orientation=column);

--创建列存本地临时表，多字段指定主键、唯一约束
drop table if exists columnd_local_tab06;
create local temp table columnd_local_tab06(id1 int,id2 int,name1 varchar,name2 char,primary key(id1,id2),constraint const_column unique(name1,name2)) with(orientation=column);

--创建范围分区列存表，多字段指定主键、唯一约束，合理报错
drop table if exists columnd_part_tab06;
create table columnd_part_tab06(id1 int primary key,id2 int primary key,name1 varchar unique,name2 char unique) with(orientation=column)
partition by range(id1)
(partition part_1 values less than(1000),
 partition part_2 values less than(2000),
 partition part_3 values less than(maxvalue));

--清理环境
drop table columns_tab06 cascade;
drop table columns_local_tab06 cascade;
drop table columns_part_tab06 cascade;
drop table columnd_local_tab06 cascade;
