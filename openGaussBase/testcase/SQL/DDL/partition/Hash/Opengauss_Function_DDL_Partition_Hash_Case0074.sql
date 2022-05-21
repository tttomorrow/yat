-- @testpoint: Hash分区表中修改多条记录

--step1：创建hash分区表 expect：成功
drop table if exists t_partition_hash_0074_01;
create table t_partition_hash_0074_01(
id int,
name varchar(100),
age int)
partition by hash(id)
(partition p1,
 partition p2);

--step2：插入数据 expect：成功插入两条数据
insert into t_partition_hash_0074_01 values( 1,  '张三', 25);
insert into t_partition_hash_0074_01 values( 2,  '张三', 25);

--step3：查看各分区数据 expect：p2分区有两条数据p1分区无数据
select * from t_partition_hash_0074_01 partition (p1);
select * from t_partition_hash_0074_01 partition (p2);

--step4：修改记录 expect：成功
update t_partition_hash_0074_01 set name = '李四' where id = 1;
update t_partition_hash_0074_01 set name = '王五' where id = 2;

--step5：查看各分区数据 expect：p2分区两条数据修改成功p1分区无数据
select * from t_partition_hash_0074_01 partition (p1);
select * from t_partition_hash_0074_01 partition (p2);

--step6：清理环境 expect：成功
drop table if exists t_partition_hash_0074_01;