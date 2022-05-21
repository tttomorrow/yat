-- @testpoint: Hash分区表结合（DEFERRABLE INITIALLY IMMEDIATE）

--step1：创建hash分区表 expect：成功
drop table if exists partition_hash_tab;
create table if not exists partition_hash_tab
(id                         number(7) primary key deferrable initially immediate,
name               varchar2(20))
partition by hash(id)
(partition p1,
 partition p2);

 --step2：插入数据 expect：成功
insert into partition_hash_tab values(1,'李四');
insert into partition_hash_tab values(2,'王五');

--step3：查询数据 expect：成功
select * from partition_hash_tab;

--step4：清理环境 expect：成功
drop table if exists partition_hash_tab cascade;