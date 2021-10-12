-- @testpoint: 执行alter table exchange后reindex

--step1:建表造数据; expect:成功
drop table if exists t_partition_0073_01;
drop table if exists t_partition_0073_02;
create table t_partition_0073_01 (a int, b int)
partition by range (a)
(
partition t_partition_0073_01_p1 values less than (10),
partition t_partition_0073_01_p2 values less than (20),
partition t_partition_0073_01_p3 values less than (30),
partition t_partition_0073_01_p4 values less than (maxvalue)
);
create index t_partition_0073_01_idx on t_partition_0073_01(a) global;
insert into t_partition_0073_01 select generate_series(0,1000), 100;

create table t_partition_0073_02 (a int, b int);
insert into t_partition_0073_02 select 13, generate_series(0,1000);

--step2:查询索引可用; expect:索引可用
select c.relname, i.indisusable
from pg_index i join pg_class c on i.indexrelid = c.oid
where i.indrelid = 't_partition_0073_01'::regclass
order by c.relname;

--step3:exchange; expect:成功
alter table t_partition_0073_01 exchange partition (t_partition_0073_01_p2) with table t_partition_0073_02 with validation;

--step4:查询索引不可用; expect:索引不可用
select c.relname, i.indisusable
from pg_index i join pg_class c on i.indexrelid = c.oid
where i.indrelid = 't_partition_0073_01'::regclass
order by c.relname;

--step5:重建索引; expect:成功
reindex table t_partition_0073_01;

--step6:查询索引不可用:重建时绕过无效索引; expect:索引不可用
select c.relname, i.indisusable
from pg_index i join pg_class c on i.indexrelid = c.oid
where i.indrelid = 't_partition_0073_01'::regclass
order by c.relname;

--step7:清理环境; expect:成功
drop table if exists t_partition_0073_01;
drop table if exists t_partition_0073_02;