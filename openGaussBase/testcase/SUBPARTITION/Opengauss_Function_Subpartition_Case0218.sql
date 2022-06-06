-- @testpoint: range_list二级分区表修改：modify_clause/exchange/merge into/move,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0218;
drop tablespace if exists ts_subpartition_0218;
create tablespace ts_subpartition_0218 relative location 'subpartition_tablespace/subpartition_tablespace_0218';

--test1: alter table modify_clause
--step2: 创建表空间; expect:成功
create table if not exists t_subpartition_0218
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
    check (col_4 is not null)
)tablespace ts_subpartition_0218
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 30 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 分区键创建索引; expect:成功
create index on t_subpartition_0218(col_1) local ;
--step4: 修改/重建指定一级分区索引不可用; expect:合理报错
alter table t_subpartition_0218 modify partition p_range_2 unusable local indexes;
alter table t_subpartition_0218 modify partition p_range_1 rebuild unusable local indexes ;

--test2: alter table exchange
--step5: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0218;
create table if not exists t_subpartition_0218
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
    check (col_4 is not null)
)tablespace ts_subpartition_0218
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 30 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step6: 创建普通表; expect:成功
drop table if exists t_subpartition_0218_01;
create table if not exists t_subpartition_0218_01
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
    check (col_4 is not null)
)tablespace ts_subpartition_0218;
--step7: 普通表插入数据; expect:成功
insert into t_subpartition_0218_01 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);

--step8: 把普通表的数据迁移到二级分区表; expect:合理报错
alter table t_subpartition_0218 exchange partition (p_range_1) with table t_subpartition_0218_01 without validation;
--step9: 查询数据; expect:成功,0条数据
select * from t_subpartition_0218;
--step10: 查询数据; expect:成功
select * from t_subpartition_0218_01;
--step11: 创建表空间; expect:成功
drop tablespace if exists ts_subpartition_0218_01;
create tablespace ts_subpartition_0218_01 relative location 'subpartition_tablespace/subpartition_tablespace_0218_01';

--test3: alter table  merge into
--step12: 修改二级分区表,把多个一级分区合并为一个一级分区; expect:合理报错
alter table t_subpartition_0218 merge partitions p_range_1,p_range_2 into partition p_range_3;
alter table t_subpartition_0218 merge partitions p_range_1,p_range_2 into partition p_range_3 tablespace ts_subpartition_0218_01;
--step13: 清空数据,插入不重复数据; expect:成功
truncate t_subpartition_0218;
insert into t_subpartition_0218 values (generate_series(-19, 19),generate_series(100,138),generate_series(200,238),generate_series(200,238));
insert into t_subpartition_0218_01 values (generate_series(-19, 19),generate_series(40,78),generate_series(80,118),generate_series(200,238));
insert into t_subpartition_0218_01 values(10000,10000,10000,10000);
--step14: merge into操作; expect:合理报错
merge into t_subpartition_0218 aaa using t_subpartition_0218_01 bbb on (aaa.col_1 = bbb.col_1)
when matched then update set aaa.col_2 = bbb.col_2 where aaa.col_1 ='10'
when not matched then insert values (bbb.col_1,bbb.col_2,bbb.col_3) where bbb.col_3=10000;

--test4: alter table  move
--step15: 修改二级分区表,移动一级分区到新的表空间; expect:合理报错
alter table t_subpartition_0218 move partition p_range_2 tablespace ts_subpartition_0218_01;
alter table t_subpartition_0218 move partition for(5) tablespace ts_subpartition_0218_01;

--test5: alter table  add partition
--step16: 修改二级分区表,添加一级分区和已有分区名重复; expect:合理报错
alter table t_subpartition_0218 add partition p_range_3 values less than( 30 ); 
--step17: 创建二级分区表; expect:成功
drop tablespace if exists t_subpartition_0218;
create table if not exists t_subpartition_0218
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
    check (col_4 is not null)
)tablespace ts_subpartition_0218
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 30 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  )
) enable row movement;
--step18: 修改二级分区表,添加一级分区和已有分区名重复; expect:合理报错
alter table t_subpartition_0218 add partition p_range_3 values less than( 50 );

--step19: 清理环境; expect:成功
drop table if exists t_subpartition_0218;
drop table if exists t_subpartition_0218_01;
drop tablespace if exists ts_subpartition_0218;
drop tablespace if exists ts_subpartition_0218_01;