-- @testpoint: 创建列存表,设置字段的收集目标set statistics,部分step合理报错

--测试点一:创建列存普通表，指定主键/唯一约束，新增字段的收集目标set statistics
--step1:测试点一,创建列存普通表,指定主键/唯一约束   expect:成功
drop table if exists t_columns_unique_index_0082_01;
create table t_columns_unique_index_0082_01(id1 smallint primary key, id2 integer unique) with(orientation=column);

--step2:测试点一,新增字段的收集目标   expect:成功
alter table t_columns_unique_index_0082_01 add statistics((id1,id2));

--step3:测试点一,查看系统表中字段统计信息   expect:无统计信息
select attname,null_frac,n_distinct,n_dndistinct from pg_stats where tablename='t_columns_unique_index_0082_01';

--step4:测试点一,插入数据，执行analyze   expect:成功
insert into t_columns_unique_index_0082_01 values(generate_series(1,1000),generate_series(1,1000));
analyze t_columns_unique_index_0082_01(id1,id2);

--step5:测试点一,再次查看系统表中字段统计信息   expect:有对应统计信息
select attname,null_frac,n_distinct,n_dndistinct from pg_stats where tablename='t_columns_unique_index_0082_01';

--step6:测试点一,再次插入数据   expect:失败
insert into t_columns_unique_index_0082_01 values(generate_series(1,1000),generate_series(1,1000));

--step7:测试点一,清理环境   expect:成功
drop table t_columns_unique_index_0082_01 cascade;



--测试点二:创建列存普通表，指定主键/唯一约束，删除字段的收集目标set statistics
--step1:测试点二,创建列存普通表,指定主键/唯一约束   expect:成功
drop table if exists t_columns_unique_index_0082_02;
create table t_columns_unique_index_0082_02(id1 smallint primary key, id2 integer unique) with(orientation=column);

--step2:测试点二,删除字段的收集目标   expect:成功
alter table t_columns_unique_index_0082_02 delete statistics((id1,id2));

--step3:测试点二,对表字段执行analyze，查看系统表中字段统计信息   expect:无统计信息
select attname,null_frac,n_distinct,n_dndistinct from pg_stats where tablename='t_columns_unique_index_0082_02';

--step4:测试点二,插入数据，执行analyze   expect:成功
insert into t_columns_unique_index_0082_02 values(generate_series(1,1000),generate_series(1,1000));
analyze t_columns_unique_index_0082_02(id1,id2);

--step5:测试点二,再次查看系统表中字段统计信息   expect:有对应统计信息
select attname,null_frac,n_distinct,n_dndistinct from pg_stats where tablename='t_columns_unique_index_0082_02';

--step6:测试点二,再次插入数据   expect:失败
insert into t_columns_unique_index_0082_02 values(generate_series(1,1000),generate_series(1,1000));

--step7:测试点二,清理环境   expect:成功
drop table t_columns_unique_index_0082_02 cascade;

