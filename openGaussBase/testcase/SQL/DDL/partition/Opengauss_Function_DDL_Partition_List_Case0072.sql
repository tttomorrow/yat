-- @testpoint: List分区表结合表约束primary key,部分测试点合理报错

--step1:创建list分区表,结合表约束;expect:成功
drop table if exists t_partition_list_0072;
create table t_partition_list_0072
(id                int,
age                int primary key,
number             int,
text               VARCHAR2(2000))
partition by list(id)
(partition p1 values(10),
 partition p2 values(20));

--step2:插入数据;expect:合理报错
insert into  t_partition_list_0072 values(10,10,10,'hahahahah');
insert into  t_partition_list_0072 values(20,10,-10,'hahahahah');

--step3:查看数据;expect:成功
select * from t_partition_list_0072;

--step4:清理环境
drop table if exists t_partition_list_0072;