-- @testpoint: hash_range二级分区表：index_parameters(primary key)/表约束(约束推迟),部分测试点合理报错

--test1: index_parameters：primary key
--step1: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0080;
create   table if not exists t_subpartition_0080
(
    col_1 int  ,
    col_2 int  not null ,
	col_3 int not null ,
    col_4 int   ,
	primary key (col_1,col_2)
)
partition by list (col_1) subpartition by range (col_2)
(
 partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_range_1_1 values less than( -10 ),
    subpartition p_range_1_2 values less than( 0 ),
    subpartition p_range_1_3 values less than( 10 ),
    subpartition p_range_1_4 values less than( 20 ),
    subpartition p_range_1_5 values less than( 50 )
  ),
  partition p_list_2 values(1,2,3,4,5,6,7,8,9,10 ),
  partition p_list_3 values(11,12,13,14,15,16,17,18,19,20)
  (
    subpartition p_range_3_1 values less than( 15 ),
    subpartition p_range_3_2 values less than( maxvalue )
  ),
    partition p_list_4 values(21,22,23,24,25,26,27,28,29,30)
  (
    subpartition p_range_4_1 values less than( -10 ),
    subpartition p_range_4_2 values less than( 0 ),
    subpartition p_range_4_3 values less than( 10 ),
    subpartition p_range_4_4 values less than( 20 ),
    subpartition p_range_4_5 values less than( 50 )
  ),
   partition p_list_5 values(31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_range_5_1 values less than( maxvalue )
  ),
   partition p_list_6 values(41,42,43,44,45,46,47,48,49,50)
   (
    subpartition p_range_6_1 values less than( -10 ),
    subpartition p_range_6_2 values less than( 0 ),
    subpartition p_range_6_3 values less than( 10 ),
    subpartition p_range_6_4 values less than( 20 ),
    subpartition p_range_6_5 values less than( 50 )
   ),
   partition p_list_7 values(default)
) enable row movement;
--step2: 插入符合(col_1,col_2)唯一约束的数据; expect:成功
insert into t_subpartition_0080 values(1,1,1,1),(5,5,5,5);
--step3: 插入不符合(col_1,col_2)唯一约束的数据; expect:合理报错
insert into t_subpartition_0080 values(1,1,1,1),(5,5,5,5);

--test2: 表约束：not null约束推迟
--step5: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0080;
create   table if not exists t_subpartition_0080
(
    col_1 int  ,
    col_2 int  not null ,
	col_3 int not null ,
    col_4 int   ,
	primary key (col_1,col_2) deferrable
)
partition by list (col_1) subpartition by range (col_2)
(
 partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_range_1_1 values less than( -10 ),
    subpartition p_range_1_2 values less than( 0 ),
    subpartition p_range_1_3 values less than( 10 ),
    subpartition p_range_1_4 values less than( 20 ),
    subpartition p_range_1_5 values less than( 50 )
  ),
  partition p_list_2 values(1,2,3,4,5,6,7,8,9,10 ),
  partition p_list_3 values(11,12,13,14,15,16,17,18,19,20)
  (
    subpartition p_range_3_1 values less than( 15 ),
    subpartition p_range_3_2 values less than( maxvalue )
  ),
    partition p_list_4 values(21,22,23,24,25,26,27,28,29,30)
  (
    subpartition p_range_4_1 values less than( -10 ),
    subpartition p_range_4_2 values less than( 0 ),
    subpartition p_range_4_3 values less than( 10 ),
    subpartition p_range_4_4 values less than( 20 ),
    subpartition p_range_4_5 values less than( 50 )
  ),
   partition p_list_5 values(31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_range_5_1 values less than( maxvalue )
  ),
   partition p_list_6 values(41,42,43,44,45,46,47,48,49,50)
   (
    subpartition p_range_6_1 values less than( -10 ),
    subpartition p_range_6_2 values less than( 0 ),
    subpartition p_range_6_3 values less than( 10 ),
    subpartition p_range_6_4 values less than( 20 ),
    subpartition p_range_6_5 values less than( 50 )
   ),
   partition p_list_7 values(default)
) enable row movement;
--step6: 开始一个事务; expect:成功
start transaction;
--step7: 设置所有约束在事务提交时检查; expect:成功
set constraints all deferred;
--step8: 插入符合(col_1,col_2)唯一约束的数据; expect:成功
insert into t_subpartition_0080 values(111,111,111),(118,118,118),(205,205,205),(505,505,505);
--step9: 插入不符合(col_1,col_2)唯一约束的数据; expect:成功
insert into t_subpartition_0080 values(111,111,111),(118,118,118),(205,205,205),(505,505,505);
--step10: 提交事务; expect:合理报错
commit;
--step11: 结束事务; expect:成功
end;
--step12: 查询数据; expect:成功，0条数据
select * from t_subpartition_0080;
--step13: 开始一个事务; expect:成功
start transaction;
--step14: 设置所有约束在事务提交时检查; expect:成功
set constraints all deferred;
--step15: 插入符合(col_1,col_2)唯一约束的数据; expect:成功
insert into t_subpartition_0080 values(111,111,111),(118,118,118),(205,205,205),(505,505,505);
--step16: 插入不符合(col_1,col_2)唯一约束的数据; expect:成功
insert into t_subpartition_0080 values(111,111,111),(118,118,118),(205,205,205),(505,505,505);
--step17: 取消所有更改; expect:成功
rollback;
--step18: 查询数据; expect:成功，0条数据
select * from t_subpartition_0080;

--step10:清理环境; expect:成功
drop table if exists t_subpartition_0080;
drop tablespace if exists ts_subpartition_0080;
