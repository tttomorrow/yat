-- @testpoint: 列存普通表结合like子句复制源表(复制约束索引)，部分step合理报错

--测试点一:创建普通列存表，指定主键约束，插入数据，使用like子句复制源表(复制约束)
--step1:测试点一,创建列存普通表,指定主键约束和唯一约束   expect:成功
drop table if exists t_columns_unique_index_0070_01;
create table t_columns_unique_index_0070_01(id1 int primary key,id2 int unique) with(orientation=column);

--step2:测试点一,插入数据   expect:成功
insert into t_columns_unique_index_0070_01 values(generate_series(1,100),generate_series(1,100));

--step3:测试点一,查看数据   expect:成功
select count(*) from t_columns_unique_index_0070_01;

--step4:测试点一,使用like子句复制源表,并且复制约束   expect:成功
drop table if exists t_columns_unique_index_0070_01_copy;
create table t_columns_unique_index_0070_01_copy (like t_columns_unique_index_0070_01 including indexes) with(orientation=column);

--step5:测试点一,将原始表数据复制到子表中   expect:成功
insert into t_columns_unique_index_0070_01_copy (select * from t_columns_unique_index_0070_01);

--step6:测试点一,查看子表是否有主键or唯一约束   expect:存在约束
select hasindexes from pg_tables where tablename='t_columns_unique_index_0070_01_copy';

--step7:测试点一,向复制表中插入已存在数据  expect:插入失败
insert into t_columns_unique_index_0070_01_copy values(generate_series(1,100),generate_series(1,100));

--step8:测试点一,清理环境   expect:成功
drop table t_columns_unique_index_0070_01 cascade;
drop table t_columns_unique_index_0070_01_copy cascade;



--测试点二:创建普通列存表，创建索引，使用like子句复制源表(复制索引)
--step1:测试点一,创建列存普通表   expect:成功
drop table if exists t_columns_unique_index_0070_02;
create table t_columns_unique_index_0070_02(id1 int,id2 int) with(orientation=column);

--step2:测试点二,创建唯一索引   expect:成功
create unique index i_columns_unique_index_0070_01 on t_columns_unique_index_0070_02 using btree(id1,id2);

--step3:测试点二,插入数据   expect:成功
insert into t_columns_unique_index_0070_02 values (generate_series(1,100),generate_series(1,100));

--step4:测试点二,使用like子句复制源表,并且复制索引   expect:成功
drop table if exists t_columns_unique_index_0070_02_copy;
create table t_columns_unique_index_0070_02_copy (like t_columns_unique_index_0070_02 including indexes) with(orientation=column);

--step5:测试点二,查看子表是否有主键or唯一约束   expect:存在索引
select hasindexes from pg_tables where tablename='t_columns_unique_index_0070_02_copy';

--step6:测试点二,将原始表数据复制到子表中   expect:成功
insert into t_columns_unique_index_0070_02_copy (select * from t_columns_unique_index_0070_02);

--step7:测试点二,向复制表中插入已存在数据  expect:插入失败
insert into t_columns_unique_index_0070_02_copy values(generate_series(1,100),generate_series(1,100));

--step8:测试点二,清理环境   expect:成功
drop table t_columns_unique_index_0070_02 cascade;
drop table t_columns_unique_index_0070_02_copy cascade;
