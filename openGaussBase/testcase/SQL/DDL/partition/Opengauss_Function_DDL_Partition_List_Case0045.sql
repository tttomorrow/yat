-- @testpoint: 分区表中添加新的字段，删除一个或多个字段，重命名分区名称，修改字段名称，修改非分区键数据类型

--step1:创建list分区表;expect:成功
drop table if exists t_partition_list_0045;
create table t_partition_list_0045(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition part_1 values(10),
 partition part_2 values(20),
 partition part_3 values(30));

--step2:增加新字段;expect:成功
alter table t_partition_list_0045 add p_stu varchar;
alter table t_partition_list_0045 add p_address varchar;

--step3:查看分区表数据;expect:成功
select * from t_partition_list_0045;

--step4:重命名分区名称;expect:成功
alter table t_partition_list_0045 rename partition  part_3 to part_4;

--step5:查看分区表数据;expect:成功
select t1.relname, partstrategy, boundaries from pg_partition t1, pg_class t2 where t1.parentid = t2.oid and t2.relname = 't_partition_list_0045' and t1.parttype = 'p' order by relname asc;

--step6:修改字段名称;expect:成功
alter table t_partition_list_0045 rename column p_name to p_add;

 --step7:修改非分区键数据类型;expect:成功
alter table t_partition_list_0045 modify p_add int;

 --step8:查看分区表数据;expect:成功
select * from t_partition_list_0045;

--step9:清理环境;expect:成功
drop table t_partition_list_0045;


