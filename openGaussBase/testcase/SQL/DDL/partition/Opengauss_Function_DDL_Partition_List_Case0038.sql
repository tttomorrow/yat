-- @testpoint: list分区表上以concurrently方式创建索引,合理报错

--step1:创建list分区表,expect成功
drop table if exists t_partition_list_0038;
create table t_partition_list_0038(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition p1 values(10),
 partition p2 values(20),
 partition p3 values(30),
 partition p4 values(40));

--step2:插入数据,expect成功
BEGIN
  for i in 1..20 LOOP
    insert into t_partition_list_0038 values(10),(20),(30),(40);
  end LOOP;
end;
/

--step3:  创建concurrently索引,expect失败
DROP INDEX IF EXISTS partition_index_01;
create index concurrently partition_index_01 ON t_partition_list_0038(p_id);

--step4:清理数据,expect成功
drop table if exists t_partition_list_0038;

