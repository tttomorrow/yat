-- @testpoint: list分区表创建多个索引

--step1:创建list分区表,expect成功
drop table if exists t_partition_list_0036;
create table t_partition_list_0036(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition p1 values(10),
 partition p2 values(20),
 partition p3 values(30),
 partition p4 values(40));

--step2:插入数据,expect成功
BEGIN
  for i in 1..20 LOOP
    insert into t_partition_list_0036 values(10),(20),(30),(40);
  end LOOP;
end;
/

--step3:并行创建索引,expect成功
drop index if exists partition_index_01;
create index partition_index_01 on t_partition_list_0036(p_id);
drop index if exists partition_index_02;
create index partition_index_02 on t_partition_list_0036(p_id);

--step4:通过索引检索表中数据,expect成功
explain select * from t_partition_list_0036 where p_id =10 ;

--step4:清理数据,expect成功
drop index if exists partition_index_01;
drop index if exists partition_index_02;
drop table if exists t_partition_list_0036;

