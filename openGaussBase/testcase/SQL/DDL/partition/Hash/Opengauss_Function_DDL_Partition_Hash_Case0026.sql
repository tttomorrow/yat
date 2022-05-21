-- @testpoint: Hash分区表创建部分索引:(psort)：合理报错

--step1：创建hash分区表 expect：成功
drop table if exists partition_hash_tab;
create table partition_hash_tab(p_id int)
partition by hash(p_id)
(partition p1,
 partition p2,
 partition p3,
 partition p4);

--step2：插入数据 expect：成功
BEGIN
  for i in 1..2000 LOOP
    insert into partition_hash_tab values(i);
  end LOOP;
end;
/

--step3：创建部分索引：psrot索引 expect：合理报错
DROP INDEX IF EXISTS partition_index_1;
CREATE INDEX partition_index_1 ON partition_hash_tab using psort(p_id) where id >5 ;

--step4：清理数据 expect：成功
drop index if exists partition_index_1;
drop table if exists partition_hash_tab cascade;