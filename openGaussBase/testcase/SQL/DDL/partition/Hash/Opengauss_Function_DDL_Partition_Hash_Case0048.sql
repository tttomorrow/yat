-- @testpoint: Hash分区表结合生成列（generated）

--step1：创建hash分区表 expect：成功
drop table if exists partition_hash_tab;
create table if not exists partition_hash_tab
(id        int,
 p_id    int generated always as ( id+1 ) stored)
partition by hash(id)
(partition p1,
 partition p2);

--step2：插入数据 expect：成功
begin
  for i in 1..20 loop
    insert into partition_hash_tab values(i);
  end loop;
end;
/

--step3：查询数据 expect：成功
select count(*) from  partition_hash_tab;

--step4：清理环境 expect：成功
drop table if exists partition_hash_tab;