-- @testpoint: range_range二级分区表：split多个分割点/add字段/drop字段/add约束,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0277;
drop tablespace if exists ts_subpartition_0277;
create tablespace ts_subpartition_0277 relative location 'subpartition_tablespace/subpartition_tablespace_0277';

--test1: alter table  split(分割点与所在分区不符)
--step2: 创建二级分区表; expect:成功
create   table if not exists t_subpartition_0277
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0277
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition p_range_2_2 values less than( 10 )
  )
) enable row movement;
--step3: 插入数据; expect:成功
insert into t_subpartition_0277 values(1,1,1,1),(4,4,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0277 values(11,1,1,1),(14,4,4,4),(15,5,5,5),(18,8,8,8),(19,9,9,9);
--step4: 修改二级分区表，split分区点高; expect:合理报错
alter table t_subpartition_0277 split subpartition p_range_1_1  at(8)  into (subpartition add_p_011 ,subpartition add_p_022);
--step5: 修改二级分区表，split分区点高低; expect:合理报错
alter table t_subpartition_0277 split subpartition p_range_1_2  at(2)  into (subpartition add_p_011 ,subpartition add_p_022);
--step6: 修改二级分区表，split一个切割点，切割为三个分区; expect:合理报错
alter table t_subpartition_0277 split subpartition p_range_1_2  at(10)  into (subpartition add_p_011,subpartition add_p_022,subpartition add_p_033);
--step7: 修改二级分区表，split切割后的名称和已有二级分区名重复; expect:合理报错
alter table t_subpartition_0277 split subpartition p_range_1_2  at(10)  into (subpartition p_range_2_1,subpartition p_range_2_2);
--step8: 修改二级分区表，split切割后的两个名称相同; expect:合理报错
alter table t_subpartition_0277 split subpartition p_range_1_2  at(10)  into (subpartition add_p_011,subpartition add_p_011);
--step9: 修改二级分区表，split切割两个分区，切割后的两个名称相同; expect:合理报错
alter table t_subpartition_0277 split subpartition p_range_1_1,p_range_1_2  at(10)  into (subpartition add_p_011,subpartition add_p_011);
--step10: 修改二级分区表，split切割值超出类型范围; expect:合理报错
alter table t_subpartition_0277 split subpartition p_range_1_2  at(1546461511131151)  into (subpartition t_subpartition_0277,subpartition add_p_011);
--step11: 修改二级分区表，正确语法split切割; expect:成功
alter table t_subpartition_0277 split subpartition p_range_1_2  at('15')  into (subpartition t_subpartition_0277,subpartition add_p_011);
--step12: 查询分区信息; expect:成功
select relname,parttype,partstrategy,indisusable,interval from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0277') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0277')) b where a.parentid = b.oid order by a.relname;

--step14: 插入数据; expect:成功
insert into t_subpartition_0277 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0277 values(1,8,1,1),(4,7,4,4),(5,8,5,5),(8,9,8,8),(9,9,9,9);
--step15: 查询切割后的分区数据; expect:成功
select * from t_subpartition_0277 subpartition(add_p_011);
--step16: 查询切割后的分区数据; expect:成功
select * from t_subpartition_0277 subpartition(t_subpartition_0277);

--test2: alter table add/drop --字段
--step17: 创建表空间; expect:成功
drop table if exists t_subpartition_0277;
create   table if not exists t_subpartition_0277
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0277
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition p_range_2_2 values less than( 10 )
  )
) enable row movement;
--step18: 修改二级分区表，添加列; expect:成功
alter table t_subpartition_0277 add column col_5 int;
--step19: 修改二级分区表，删除列; expect:成功
alter table t_subpartition_0277 drop column col_5 ;

--test3: alter table add --约束
--step20: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0041;
create   table if not exists t_subpartition_0277
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0277
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition p_range_2_2 values less than( 10 )
  )
) enable row movement;
--step21: 修改二级分区表，添加check约束; expect:成功
alter table t_subpartition_0277 add constraint constraint_check check (col_3 is not null);

--step22: 清理环境; expect:成功
drop table if exists t_subpartition_0277;
drop tablespace if exists ts_subpartition_0277;