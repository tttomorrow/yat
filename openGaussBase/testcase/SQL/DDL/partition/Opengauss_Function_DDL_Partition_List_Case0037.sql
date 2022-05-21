-- @testpoint: list分区表创建部分索引(psort),合理报错

--step1:创建list分区表,expect成功
drop table if exists t_partition_list_0037;
create table t_partition_list_0037(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition p1 values(10),
 partition p2 values(20),
 partition p3 values(30),
 partition p4 values(40));

--step2:插入数据,expect成功
BEGIN
  for i in 1..20 LOOP
    insert into t_partition_list_0037 values(10),(20),(30),(40);
  end LOOP;
end;
/

--step3: 创建部分索引psrot索引,expect失败
DROP INDEX IF EXISTS partition_index_01;
CREATE INDEX partition_index_01 ON t_partition_list_0037 using psort(p_id) where id =10;

--step4:清理数据,expect成功
drop table if exists t_partition_list_0037;

