-- @testpoint: range_list二级分区表：索引,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0251;
drop tablespace if exists ts_subpartition_0251;
create tablespace ts_subpartition_0251 relative location 'subpartition_tablespace/subpartition_tablespace_0251';
drop tablespace if exists ts_subpartition_0251_01;
create tablespace ts_subpartition_0251_01 relative location 'subpartition_tablespace/subpartition_tablespace_0251_01';

--step2: 创建二级分区表; expect:成功
create table t_subpartition_0251
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0251
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
--step3: 插入数据; expect:成功
insert into t_subpartition_0251 values (generate_series(-100, 100),generate_series(400, 200,-1),generate_series(700, 500,-1));
insert into t_subpartition_0251 values (generate_series(200, 400),generate_series(800, 600,-1),generate_series(900, 700,-1));
insert into t_subpartition_0251 values (generate_series(2200, 4400),generate_series(4800, 2600,-1),generate_series(4900, 2700,-1));

--step4: 创建唯一索引; expect:成功
create unique index on t_subpartition_0251(col_1);
--step5: 索引键不包含分区键创建local索引; expect:合理报错
create unique index on t_subpartition_0251(col_2) local;
create unique index on t_subpartition_0251(col_1,col_2);

--step6: 索引键不包含分区键创建local索引; expect:合理报错
create  unique index on t_subpartition_0251(col_1) local;
--step7: 已存在local索引,创建global索引; expect:合理报错
create unique index on t_subpartition_0251(col_1,col_2) global;
--step8: 删除索引; expect:成功
drop index t_subpartition_0251_col_1_col_2_idx;
--step9: 不存在local索引,创建global索引; expect:成功
create unique index on t_subpartition_0251(col_1,col_2) global;
--step10: 删除索引; expect:成功
drop index t_subpartition_0251_col_1_col_2_tableoid_idx;

--step11: 创建不同部分索引; expect:成功
create unique index  on t_subpartition_0251 (col_1,col_2 nulls first) tablespace ts_subpartition_0251_01 where col_2 < 4;
--step12: 查看执行计划; expect:成功
explain  analyze select * from t_subpartition_0251 where col_2 in  (select col_1 from t_subpartition_0251  where col_1 >10 and col_1<100 ) and col_2 <4 order by 1 limit 100;                                                                              query plan

--step13: 创建不同部分索引; expect:合理报错
create unique index  on t_subpartition_0251 (col_2 nulls first) tablespace ts_subpartition_0251_01 where col_2 < 4;
--step14: 创建不同部分索引; expect:成功
create unique index  on t_subpartition_0251 (col_1,col_2 nulls first) tablespace ts_subpartition_0251_01 where col_2 is not null;
--step15: 查看执行计划; expect:成功
explain  analyze select * from t_subpartition_0251 where col_2 in  (select col_1 from t_subpartition_0251  where col_1 >10 and col_1<100 ) and col_2 <4 order by 1 limit 100;

--step16: 创建不同部分索引; expect:成功
create unique index  on t_subpartition_0251 (col_1,col_2 nulls first) tablespace ts_subpartition_0251_01 where col_2 is  null;
--step17: 查看执行计划; expect:成功
explain  analyze select * from t_subpartition_0251 where col_2 in  (select col_1 from t_subpartition_0251  where col_1 >10 and col_1<100 ) and col_2 is null order by 1 limit 100;

--step18: 创建不同部分索引; expect:合理报错
create unique index  on t_subpartition_0251 (col_1,col_2 nulls first) tablespace ts_subpartition_0251_01 where col_2 in  (select col_1 from t_subpartition_0251  where col_1 >10 and col_1<100 );
--step19: 创建不同部分索引; expect:成功
create unique index  on t_subpartition_0251 (col_1,col_2 nulls first) tablespace ts_subpartition_0251_01 where col_2 in  (100,200,300 );
--step20: 查看执行计划; expect:成功
explain  analyze select * from t_subpartition_0251 where col_2 in  (select col_1 from t_subpartition_0251  where col_1 >10 and col_1<100 ) and col_2  in  (100,200,300 ) order by 1 limit 100;
--step21: 查看执行计划; expect:成功,走索引
explain  analyze select * from t_subpartition_0251 where col_2 in  (select col_1 from t_subpartition_0251  where col_1 >10 and col_1<100 ) and col_2  in  (100,200 ) order by 1 limit 100;

--step22: 创建不同部分索引; expect:成功
create unique index  on t_subpartition_0251 (col_1,col_2 nulls first) tablespace ts_subpartition_0251_01 where col_2 = 100;
--step23: 查看执行计划; expect:成功
explain  analyze select * from t_subpartition_0251 where col_2 in  (select col_1 from t_subpartition_0251  where col_1 >10 and col_1<100 ) and col_2 = 100 order by 1 limit 100;

--test1:  method
--step25: 使用不同method创建索引; expect:合理报错
create index on t_subpartition_0251 using gin(col_2 asc) local;
--step26: 使用不同method创建索引; expect:合理报错
create index on t_subpartition_0251 using gist(col_2 asc) local;
--step27: 使用不同method创建索引; expect:合理报错
create index on t_subpartition_0251 using psort(col_2 asc) local;
--step28: 使用不同method创建索引; expect:成功
create index on t_subpartition_0251 using btree(col_2 asc) local;
--step29: 查看执行计划; expect:成功
explain  analyze select * from t_subpartition_0251 where col_2 in  (select col_1 from t_subpartition_0251  where col_1 >10 and col_1<100) order by 1 limit 100;

--step30: 创建索引; expect:成功
create unique index t_subpartition_0251_ind_04 on t_subpartition_0251 (col_1 nulls first) ;
--step31: 修改索引; expect:合理报错
alter table t_subpartition_0251 add constraint t_subpartition_0251_pkey primary key using index t_subpartition_0251_ind_04;
--step32: 删除索引; expect:成功
drop index t_subpartition_0251_col_2_idx;
--step33: 创建索引; expect:成功
create unique index t_subpartition_0251_ind_05 on t_subpartition_0251 (col_2 ) ;
--step34: 修改索引; expect:成功
alter table t_subpartition_0251 add constraint t_subpartition_0251_pkey primary key using index t_subpartition_0251_ind_05;
--step35: 查看执行计划; expect:成功
explain  analyze  select * from t_subpartition_0251 where col_2 in  (select col_1 from t_subpartition_0251  where col_1 >10 and col_1<100) order by 1 limit 100;

--step36: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0251;
create table t_subpartition_0251
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0251
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
--step37: 插入数据; expect:成功
insert into t_subpartition_0251 values (generate_series(-100, 100),generate_series(400, 200,-1),generate_series(700, 500,-1));
insert into t_subpartition_0251 values (generate_series(200, 400),generate_series(800, 600,-1),generate_series(900, 700,-1));
insert into t_subpartition_0251 values (generate_series(2200, 4400),generate_series(4800, 2600,-1),generate_series(4900, 2700,-1));
--step38: 创建索引; expect:成功
create index on t_subpartition_0251(col_2) local;
--step39: 查看分析计划; expect:使用 local索引t_subpartition_0251_col_2_idx
explain  analyze select * from t_subpartition_0251 where col_2 in  (select col_1 from t_subpartition_0251  where col_1 >10 and col_1<100) order by 1 limit 100;
--step40: 设置local索引某分区索引不可用; expect:成功
alter index t_subpartition_0251_col_2_idx modify partition p_list_4_1_col_2_idx  unusable;
--step41: 查看分析计划; expect:不使用 local索引t_subpartition_0251_col_2_idx
explain  analyze select * from t_subpartition_0251 where col_2 in  (select col_1 from t_subpartition_0251  where col_1 >10 and col_1<100) order by 1 limit 100;
--step42: 重置分区索引可用; expect:成功
alter index t_subpartition_0251_col_2_idx rebuild  partition p_list_4_1_col_2_idx ;
--step43: 重命名分区索引; expect:成功
alter index t_subpartition_0251_col_2_idx rename partition p_list_4_1_col_2_idx to  ztt;
--step44: collation索引; expect:合理报错
create index index_01 on i_subpartition_0251(col_2) collation local;
--step45: 二级分区键创建local索引,指定索引分区名的数量不正确; expect:合理报错
drop index if exists i_subpartition_0251;
create index i_subpartition_0251 on t_subpartition_0251(col_2)local(partition p_range_1,partition p_range_2,partition p_range_3,partition p_range_4,partition p_range_5);

--step46: 清理环境; expect:成功
drop table if exists t_subpartition_0251_01;
drop table if exists t_subpartition_0251;
drop tablespace if exists ts_subpartition_0251;
drop tablespace if exists ts_subpartition_0251_01;