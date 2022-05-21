-- @testpoint: List分区表结合（DEFERRABLE )

--step1:创建list分区表deferrable initially immediate;expect:成功
drop table if exists t_partition_list_0060_01;
create table if not exists t_partition_list_0060_01
(id                number(7) primary key deferrable initially deferred,
name               varchar2(20))
partition by list(id)
(partition p1 values(10),
 partition p2 values(20));

--step2:创建list分区表deferrable initially immediate;expect:成功
drop table if exists t_partition_list_0060_02;
create table if not exists t_partition_list_0060_02
(id                number(7) primary key deferrable initially immediate,
name               varchar2(20))
partition by list(id)
(partition p1 values(10),
 partition p2 values(20));

