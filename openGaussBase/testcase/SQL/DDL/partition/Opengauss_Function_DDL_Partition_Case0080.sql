-- @testpoint: 分区表的数据迁移到普通表


--step1:创建范围分区表;  expect:成功
drop table if exists t_partition_0080_01;
create table t_partition_0080_01(c_id int,c_name varchar(32))
partition by range (c_id)
(partition p1 values less than (101),
 partition p2 values less than (201),
 partition p3 values less than (301));

--step2:插入数据;  expect:成功
insert into t_partition_0080_01 values (generate_series(1,300),'ab');

--step3:创建普通表;  expect:成功
drop table if exists t_partition_0080_02;
create table t_partition_0080_02 (like t_partition_0080_01 including reloptions);

--step4:分区表的数据迁移到普通表;  expect:成功
alter table t_partition_0080_01 exchange partition (p1) with table t_partition_0080_02;

--step5:查看普通表数据;  expect:成功
select count(*) from t_partition_0080_02;

--step6:清理环境;  expect:成功
drop table t_partition_0080_01 cascade;
drop table t_partition_0080_02 cascade;