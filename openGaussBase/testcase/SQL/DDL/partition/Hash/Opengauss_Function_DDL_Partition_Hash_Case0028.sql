-- @testpoint: hash分区表以隔离级别为read committed，访问模式为read write启动事务

--step1：创建hash分区表 expect：成功
drop table if exists partition_hash_tab;
create table partition_hash_tab(p_id int)
partition by hash(p_id)
(partition p1,
 partition p2,
 partition p3,
 partition p4);

--step2：以隔离级别为read committed，访问模式为read write启动事务插入数据 expect：成功
start transaction isolation level read committed read write;
insert into partition_hash_tab values (001);
insert into partition_hash_tab values (002);
insert into partition_hash_tab values (003);
insert into partition_hash_tab values (004);
end;

--step3：查看数据 expect：成功
select * from partition_hash_tab;

--step4：清理数据 expect：成功
drop table if exists partition_hash_tab cascade;