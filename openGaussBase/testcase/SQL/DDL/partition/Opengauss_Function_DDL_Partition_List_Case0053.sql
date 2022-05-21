-- @testpoint: List分区表结合LIKE INCLUDING CONSTRAINTS参数，部分测试点合理报错

--step01:创建list分区表;expect:成功
drop table if exists t_partition_list_0053_01;
drop table if exists t_partition_list_0053_02;
create table t_partition_list_0053_01
(id              number(7) ,
p_age            int check(p_age>0) ,
 filename        varchar2(255),
 text            varchar2(2000))
partition by  list(id)
(partition p1 values(1),
 partition p2 values(2),
 partition p3 values(3));

--step02:插入数据;expect:合理报错
insert into t_partition_list_0053_01(id,p_age,text ) values(1,15,'老师');
insert into t_partition_list_0053_01(id,p_age,text ) values(2,0,'老师');
insert into t_partition_list_0053_01(id,p_age,text ) values(2,-15,'老师');

--step03:查看数据;expect:成功
select * from t_partition_list_0053_01;

--step04:使用like参数建表;expect:成功
create table t_partition_list_0053_02 (like  t_partition_list_0053_01 including constraints);

--step05:插入数据;expect:合理报错
insert into t_partition_list_0053_02 (id,p_age,text ) values(1,15,'老师');
insert into t_partition_list_0053_02 (id,p_age,text ) values(2,0,'老师');
insert into t_partition_list_0053_02 (id,p_age,text ) values(2,-15,'老师');

--step06:查看数据;expect:成功
select * from t_partition_list_0053_02 ;

--step07:清理环境;expect:成功
drop table if exists t_partition_list_0053_01;
drop table if exists t_partition_list_0053_02;