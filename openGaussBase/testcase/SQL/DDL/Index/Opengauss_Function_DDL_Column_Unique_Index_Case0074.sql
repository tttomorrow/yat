-- @testpoint: 列存分区表结合create table as子句复制源表，不支持复制分区

--创建列存范围分区表，指定主键约束，插入数据，使用create table as子句复制源分区表
--step1:创建列存范围分区表,指定主键约束   expect:成功
drop table if exists t_columns_unique_index_0074;
create table t_columns_unique_index_0074(id int primary key,name varchar(20)) with(orientation=column)
partition by range(id)
(partition part_1 values less than(100),
 partition part_2 values less than(200),
 partition part_3 values less than(300),
 partition part_4 values less than(400),
 partition part_5 values less than(maxvalue));

--step2:插入数据   expect:成功
insert into t_columns_unique_index_0074 values(generate_series(1,1000),'a_'||generate_series(1,1000));

--step3:查看数据   expect:成功
select count(*) from t_columns_unique_index_0074;

--step4:使用create table as子句复制源表   expect:成功
drop table if exists t_columns_unique_index_0074_copy;
create table t_columns_unique_index_0074_copy with (orientation=column) as table t_columns_unique_index_0074;

--step5:查看子表的分区信息  expect:子表不存在分区信息
select relname, parttype, boundaries from pg_partition where parentid = (select oid from pg_class where relname = 't_columns_unique_index_0074_copy') order by relname;

--step6:清理环境   expect:成功
drop table t_columns_unique_index_0074 cascade;
drop table t_columns_unique_index_0074_copy cascade;

