-- @testpoint: 列存分区表结合like子句复制源表(不复制约束索引)，部分step合理报错

--测试点一:创建列存范围分区表，指定主键约束，插入数据，使用like子句复制源表(不复制约束)
--step1:测试点一,创建列存范围分区表,指定主键约束   expect:成功
drop table if exists t_columns_unique_index_0071_01;
create table t_columns_unique_index_0071_01(id int primary key,name varchar(20)) with(orientation=column)
partition by range(id)
(partition part_1 values less than(100),
 partition part_2 values less than(200),
 partition part_3 values less than(300),
 partition part_4 values less than(400),
 partition part_5 values less than(maxvalue));

--step2:测试点一,插入数据   expect:成功
insert into t_columns_unique_index_0071_01 values(generate_series(1,1000),'a_'||generate_series(1,1000));

--step3:测试点一,查看数据   expect:成功
select count(*) from t_columns_unique_index_0071_01;

--step4:测试点一,使用like子句复制源表,并且不复制约束   expect:成功
drop table if exists t_columns_unique_index_0071_01_copy;
create table t_columns_unique_index_0071_01_copy (like t_columns_unique_index_0071_01 including partition) with(orientation=column);

--step5:测试点一,查看子表的分区信息  expect:成功
select relname, parttype, boundaries from pg_partition where parentid = (select oid from pg_class where relname = 't_columns_unique_index_0071_01_copy') order by relname;

--step6:测试点一,将原始表数据复制到子表中   expect:成功
insert into t_columns_unique_index_0071_01_copy (select * from t_columns_unique_index_0071_01);

--step7:测试点一,查看子表是否有主键约束   expect:无约束
select hasindexes from pg_tables where tablename='t_columns_unique_index_0071_01_copy';

--step8:测试点一,向子表新增主键约束   expect:成功
alter table t_columns_unique_index_0071_01_copy add primary key(id);

--step9:测试点一,向复制表中插入已存在数据  expect:插入失败
insert into t_columns_unique_index_0071_01_copy values(generate_series(1,100),generate_series(1,100));

--step10:测试点一,清理环境   expect:成功
drop table t_columns_unique_index_0071_01 cascade;
drop table t_columns_unique_index_0071_01_copy cascade;


--测试点二:创建列存范围分区表，指定唯一约束，插入数据，使用like子句复制源表(不复制约束)
--step1:测试点二,创建列存范围分区表,指定唯一约束   expect:成功
drop table if exists t_columns_unique_index_0071_02;
create table t_columns_unique_index_0071_02(id int unique,name varchar(20)) with(orientation=column)
partition by range(id)
(partition part_1 values less than(100),
 partition part_2 values less than(200),
 partition part_3 values less than(300),
 partition part_4 values less than(400),
 partition part_5 values less than(maxvalue));

--step2:测试点二,插入数据   expect:成功
insert into t_columns_unique_index_0071_02 values(generate_series(1,1000),'a_'||generate_series(1,1000));

--step3:测试点二,查看数据   expect:成功
select count(*) from t_columns_unique_index_0071_02;

--step4:测试点二,使用like子句复制源表,并且不复制约束   expect:成功
drop table if exists t_columns_unique_index_0071_02_copy;
create table t_columns_unique_index_0071_02_copy (like t_columns_unique_index_0071_02 including partition) with(orientation=column);

--step5:测试点二,查看子表的分区信息  expect:成功
select relname, parttype, boundaries from pg_partition where parentid = (select oid from pg_class where relname = 't_columns_unique_index_0071_02_copy') order by relname;

--step6:测试点二,将原始表数据复制到子表中   expect:成功
insert into t_columns_unique_index_0071_02_copy (select * from t_columns_unique_index_0071_02);

--step7:测试点二,查看子表是否有唯一约束   expect:无约束
select hasindexes from pg_tables where tablename='t_columns_unique_index_0071_02_copy';

--step8:测试点二,向子表新增唯一约束   expect:成功
alter table t_columns_unique_index_0071_02_copy add constraint cons_71 unique(id);

--step9:测试点二,向复制表中插入已存在数据  expect:插入失败
insert into t_columns_unique_index_0071_02_copy values(generate_series(1,100),generate_series(1,100));

--step10:测试点二,清理环境   expect:成功
drop table t_columns_unique_index_0071_02 cascade;
drop table t_columns_unique_index_0071_02_copy cascade;


--测试点三:创建列存范围分区表，创建索引，使用like子句复制源表(不复制索引)
--step1:测试点三,创建列存普通表   expect:成功
drop table if exists t_columns_unique_index_0071_03;
create table t_columns_unique_index_0071_03(id int unique,name varchar(20)) with(orientation=column)
partition by range(id)
(partition part_1 values less than(100),
 partition part_2 values less than(200),
 partition part_3 values less than(300),
 partition part_4 values less than(400),
 partition part_5 values less than(maxvalue));

--step2:测试点三,创建唯一索引   expect:成功
create unique index i_columns_unique_index_0071_01 on t_columns_unique_index_0071_03 using btree(id) local;

--step3:测试点三,插入数据   expect:成功
insert into t_columns_unique_index_0071_03 values (generate_series(1,100),generate_series(1,100));

--step4:测试点三,使用like子句复制源表,并且不复制索引   expect:成功
drop table if exists t_columns_unique_index_0071_03_copy;
create table t_columns_unique_index_0071_03_copy (like t_columns_unique_index_0071_03 including partition) with(orientation=column);

--step5:测试点三,查看子表的分区信息  expect:成功
select relname, parttype, boundaries from pg_partition where parentid = (select oid from pg_class where relname = 't_columns_unique_index_0071_03_copy') order by relname;

--step6:测试点三,将原始表数据复制到子表中   expect:成功
insert into t_columns_unique_index_0071_03_copy (select * from t_columns_unique_index_0071_03);

--step7:测试点三,查看子表是否有主键or唯一约束   expect:无索引
select hasindexes from pg_tables where tablename='t_columns_unique_index_0071_03_copy';

--step8:测试点三,向子表创建唯一索引   expect:成功
create unique index i_columns_unique_index_0071_02 on t_columns_unique_index_0071_03_copy using btree(id) local;

--step9:测试点三,向复制表中插入已存在数据  expect:插入失败
insert into t_columns_unique_index_0071_03_copy values(generate_series(1,100),generate_series(1,100));

--step10:测试点三,清理环境   expect:成功
drop table t_columns_unique_index_0071_03 cascade;
drop table t_columns_unique_index_0071_03_copy cascade;
