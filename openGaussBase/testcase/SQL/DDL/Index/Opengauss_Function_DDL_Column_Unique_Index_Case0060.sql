-- @testpoint: 列存分区表创建唯一索引，添加新的分区，部分测试点合理报错

--测试点一:创建唯一索引后,增加新的分区,插入数据
--step1:测试点一,创建列存范围分区表   expect:成功
drop table if exists t_columns_unique_index_0060_01;
create table t_columns_unique_index_0060_01(id1 int,id2 int,id3 int) with(orientation=column)
partition by range(id1)
(partition p01 values less than(1000),
 partition p02 values less than(2000),
 partition p03 values less than(3000),
 partition p04 values less than(5000),
 partition p05 values less than(6000));

--step2:测试点一,创建本地唯一索引   expect:成功
create unique index i_columns_unique_index_0060_01 on t_columns_unique_index_0060_01 using btree(id1,id2,id3) local;

--step3:测试点一,增加新的分区   expect:成功
alter table t_columns_unique_index_0060_01 add partition p06 values less than(6500);

--step4:测试点一,向新增分区插入数据   expect:成功
insert into t_columns_unique_index_0060_01 values(generate_series(1,6100),generate_series(1,6100),generate_series(1,6100));

--step5:测试点一,清理环境   expect:成功
drop table t_columns_unique_index_0060_01 cascade;


--测试点二:创建唯一索引后,插入数据,增加新的分区,清空表数据后再次插入数据
--step1:测试点二,创建列存范围分区表   expect:成功
drop table if exists t_columns_unique_index_0060_02;
create table t_columns_unique_index_0060_02(id1 int,id2 int,id3 int) with(orientation=column)
partition by range(id1)
(partition p01 values less than(1000),
 partition p02 values less than(2000),
 partition p03 values less than(3000),
 partition p04 values less than(5000),
 partition p05 values less than(6000));

--step2:测试点二,创建本地唯一索引   expect:成功
create unique index i_columns_unique_index_0060_02 on t_columns_unique_index_0060_02 using btree(id1,id2,id3) local;

--step3:测试点二,插入数据   expect:成功
insert into t_columns_unique_index_0060_02 values(generate_series(1,5000),generate_series(1,5000),generate_series(1,5000));

--step4:测试点二,增加新的分区   expect:成功
alter table t_columns_unique_index_0060_02 add partition p07 values less than(7500);

--step5:测试点二,清空表数据  expect:成功
truncate table t_columns_unique_index_0060_02;

--step6:测试点二,向新增分区插入数据   expect:成功
insert into t_columns_unique_index_0060_02 values(generate_series(1,7000),generate_series(1,7000),generate_series(1,7000));

--step7:测试点二,清理环境   expect:成功
drop table t_columns_unique_index_0060_02 cascade;


--测试点三:插入数据后增加新的分区,创建唯一索引,清再次插入数据
--step1:测试点三,创建列存范围分区表   expect:成功
drop table if exists t_columns_unique_index_0060_03;
create table t_columns_unique_index_0060_03(id1 int,id2 int,id3 int) with(orientation=column)
partition by range(id1)
(partition p01 values less than(1000),
 partition p02 values less than(2000),
 partition p03 values less than(3000),
 partition p04 values less than(5000),
 partition p05 values less than(6000));

--step2:测试点三,插入数据   expect:成功
insert into t_columns_unique_index_0060_03 values(generate_series(1,5000),generate_series(1,5000),generate_series(1,5000));

--step3:测试点三,增加新的分区   expect:成功
alter table t_columns_unique_index_0060_03 add partition p07 values less than(7500);

--step4:测试点三,插入数据   expect:成功
insert into t_columns_unique_index_0060_03 values(6000,6000,6000);

--step5:测试点三,创建本地唯一索引   expect:成功
create unique index i_columns_unique_index_0060_03 on t_columns_unique_index_0060_03 using btree(id1,id2,id3) local;

--step6:测试点三,向新增分区插入数据   expect:成功
insert into t_columns_unique_index_0060_03 values(7000,7000,7000);

--step7:测试点三,清理环境   expect:成功
drop table t_columns_unique_index_0060_03 cascade;



--测试点四:增加新的字段,创建唯一索引,插入数据
--step1:测试点四,创建列存范围分区表   expect:成功
drop table if exists t_columns_unique_index_0060_04;
create table t_columns_unique_index_0060_04(id1 int,id2 int,id3 int) with(orientation=column)
partition by range(id1)
(partition p01 values less than(1000),
 partition p02 values less than(2000),
 partition p03 values less than(3000),
 partition p04 values less than(5000),
 partition p05 values less than(6000));

--step2:测试点四,新增字段，创建唯一索引  expect:失败
alter table t_columns_unique_index_0060_04 add column id4 text unique;

--step3:测试点四,清理环境   expect:成功
drop table t_columns_unique_index_0060_04 cascade;

