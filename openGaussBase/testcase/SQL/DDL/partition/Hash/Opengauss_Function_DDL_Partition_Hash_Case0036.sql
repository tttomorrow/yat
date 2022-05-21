-- @testpoint: Hash分区表结合COLLATE子句(POSIX)

--step1：创建hash分区表，指定COLLATE子句(POSIX) expect：成功
drop table if exists partition_hash_tab;
create table partition_hash_tab(
p_id int,
p_name varchar(10) COLLATE "POSIX")
partition by hash(p_id)
(partition p1,
 partition p2);

--step2：插入数据 expect：成功
insert into partition_hash_tab values(1,'李四'),
(2,'王五');

--step3：查询数据 expect：成功
select * from partition_hash_tab;

--step4：清理环境 expect：成功
drop table if exists partition_hash_tab;