-- @testpoint: 列存分区表创建唯一索引，合并原有分区

--测试点一:创建本地唯一索引后合并原有表分区,插入数据
--step1:测试点一,创建列存范围分区表   expect:成功
drop table if exists t_columns_unique_index_0062_01;
create table t_columns_unique_index_0062_01(id1 int,id2 int,id3 int) with(orientation=column)
partition by range(id1)
(partition p01 values less than(1000),
 partition p02 values less than(2000),
 partition p03 values less than(3000),
 partition p04 values less than(5000),
 partition p05 values less than(6000));

--step2:测试点一,创建本地唯一索引   expect:成功
create unique index i_columns_unique_index_0062_01 on t_columns_unique_index_0062_01 using btree(id1,id2,id3) local;

--step3:测试点一,合并原有分区   expect:成功
alter table t_columns_unique_index_0062_01 merge partitions p04, p05 into partition p06;

--step4:测试点一,查看分区信息   expect:成功
select relname from pg_partition
where parentid = (select parentid from pg_partition where relname = 't_columns_unique_index_0062_01')
and parttype = 'p' order by boundaries desc;

--step5:测试点一,向新增分区插入数据   expect:成功
insert into t_columns_unique_index_0062_01 values(generate_series(1,5999),generate_series(1,5999),generate_series(1,5999));

--step6:测试点一,清理环境   expect:成功
drop table t_columns_unique_index_0062_01 cascade;


--测试点二:合并原有表分区后创建本地唯一索引,插入数据
--step1:测试点一,创建列存范围分区表  expect:成功
drop table if exists t_columns_unique_index_0062_02;
create table t_columns_unique_index_0062_02(id1 int,id2 int,id3 int) with(orientation=column)
partition by range(id1)
(partition p01 values less than(1000),
 partition p02 values less than(2000),
 partition p03 values less than(3000),
 partition p04 values less than(5000),
 partition p05 values less than(6000));

--step2:测试点二,合并原有分区   expect:成功
alter table t_columns_unique_index_0062_02 merge partitions p04, p05 into partition p06;

--step3:测试点二,查看分区信息   expect:成功
select relname from pg_partition
where parentid = (select parentid from pg_partition where relname = 't_columns_unique_index_0062_02')
and parttype = 'p' order by boundaries desc;

--step4:测试点二,创建本地唯一索引   expect:成功
create unique index i_columns_unique_index_0062_02 on t_columns_unique_index_0062_02 using btree(id1,id2,id3) local;

--step5:测试点二,向新增分区插入数据   expect:成功
insert into t_columns_unique_index_0062_02 values(generate_series(1,5999),generate_series(1,5999),generate_series(1,5999));

--step6:测试点二,清理环境   expect:成功
drop table t_columns_unique_index_0062_02 cascade;


