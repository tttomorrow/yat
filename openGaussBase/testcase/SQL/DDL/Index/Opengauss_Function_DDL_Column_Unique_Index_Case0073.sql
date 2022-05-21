-- @testpoint: 列存普通表结合create table as子句复制源表,部分step合理报错

--测试点一:创建普通列存表，指定主键约束，插入数据，使用create table as子句复制源表
--step1:测试点一,创建列存普通表,指定主键约束和唯一约束   expect:成功
drop table if exists t_columns_unique_index_0073_01;
create table t_columns_unique_index_0073_01(id1 int primary key,id2 int unique) with(orientation=column);

--step2:测试点一,插入数据   expect:成功
insert into t_columns_unique_index_0073_01 values(generate_series(1,100),generate_series(1,100));

--step3:测试点一,查看数据   expect:成功
select count(*) from t_columns_unique_index_0073_01;

--step4:测试点一,使用create table as子句复制源表   expect:成功
drop table if exists t_columns_unique_index_0073_01_copy;
create table t_columns_unique_index_0073_01_copy with (orientation=column) as table t_columns_unique_index_0073_01;

--step5:测试点一,查看子表是否有主键or唯一约束   expect:无约束
select hasindexes from pg_tables where tablename='t_columns_unique_index_0073_01_copy';

--step6:测试点一,向子表新增唯一约束or主键约束   expect:成功
alter table t_columns_unique_index_0073_01_copy add constraint cons_69 unique(id1);
alter table t_columns_unique_index_0073_01_copy add primary key(id2);

--step7:测试点一,向复制表中插入已存在数据  expect:插入失败
insert into t_columns_unique_index_0073_01_copy values(generate_series(1,100),generate_series(1,100));

--step8:测试点一,清理环境   expect:成功
drop table t_columns_unique_index_0073_01 cascade;
drop table t_columns_unique_index_0073_01_copy cascade;



--测试点二:创建普通列存表，创建唯一索引，插入数据，使用create table as子句复制源表
--step1:测试点二,创建列存普通表,指定主键约束和唯一约束   expect:成功
drop table if exists t_columns_unique_index_0073_02;
create table t_columns_unique_index_0073_02(id1 int primary key,id2 int unique) with(orientation=column);

--step2:测试点二,创建唯一索引   expect:成功
create unique index i_columns_unique_index_0073_01 on t_columns_unique_index_0073_02 using btree(id1);

--step3:测试点二,插入数据   expect:成功
insert into t_columns_unique_index_0073_02 values(generate_series(1,100),generate_series(1,100));

--step4:测试点二,查看数据   expect:成功
select count(*) from t_columns_unique_index_0073_02;

--step5:测试点二,使用create table as子句复制源表   expect:成功
drop table if exists t_columns_unique_index_0073_02_copy;
create table t_columns_unique_index_0073_02_copy with (orientation=column) as table t_columns_unique_index_0073_02;

--step6:测试点二,查看子表是否有主键or唯一约束   expect:无约束
select hasindexes from pg_tables where tablename='t_columns_unique_index_0073_02_copy';

--step7:测试点二,向子表新增唯一索引束   expect:成功
create unique index i_columns_unique_index_0073_02 on t_columns_unique_index_0073_02_copy using btree(id1);

--step8:测试点二,向复制表中插入已存在数据  expect:插入失败
insert into t_columns_unique_index_0073_02_copy values(generate_series(1,100),generate_series(1,100));

--step9:测试点二,清理环境   expect:成功
drop table t_columns_unique_index_0073_02 cascade;
drop table t_columns_unique_index_0073_02_copy cascade;


