-- @testpoint: List分区表中删除字段

--step1:创建list分区表;expect:成功
drop table if exists t_partition_list_0065;
create table t_partition_list_0065(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition p1 values(10),
 partition p2 values(20),
 partition p3 values(30));

--step3:插入数据;expect:成功
insert into t_partition_list_0065 values( 10,  '张三', 25);
insert into t_partition_list_0065 values( 10,  '张三', 26);
insert into t_partition_list_0065 values( 20,  '张三', 27);
insert into t_partition_list_0065 values( 20,  '张三', 28);

--step4:删除字段;expect:成功
alter table t_partition_list_0065 drop column if exists p_age;

--step6:查看分区数据;expect:成功
select * from t_partition_list_0065 order by p_id asc;

--step7:清理环境;expect:成功
drop table if exists t_partition_list_0065;





