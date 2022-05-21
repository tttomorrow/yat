-- @testpoint: range_range二级分区表：索引/表名和系统表同名,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0307;
drop tablespace if exists ts_subpartition_0307;
create tablespace ts_subpartition_0307 relative location 'subpartition_tablespace/subpartition_tablespace_0307';
drop tablespace if exists ts_subpartition_0307_01;
create tablespace ts_subpartition_0307_01 relative location 'subpartition_tablespace/subpartition_tablespace_0307_01';

--step2: 创建二级分区表; expect:成功
create table t_subpartition_0307
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int ,
    col_5 int ,
    col_6 int ,
    col_7 int ,
    col_8 int ,
    col_9 int ,
    col_10 int ,
    col_11 int ,
    col_12 int ,
    col_13 int ,
    col_14 smallint    ,
    col_15 integer    ,
    col_16 bigint    ,
    col_17 decimal    ,
    col_18 numeric    ,
    col_19 real    ,
    col_20 double precision    ,
    col_21 character    ,
    col_22 varchar(10)    ,
    col_23 character(10)    ,
    col_24 char(10)    ,
    col_25 char    ,
    col_26 text    ,
    col_27 nvarchar2    ,
    col_28 name    ,
    col_29 timestamp without time zone    ,
    col_30 timestamp with time zone    ,
    col_31 date,
    col_32 int ,
    col_33 int ,
    col_34 int ,
    col_35 int ,
    col_36 int
)
tablespace ts_subpartition_0307
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_range_1_1 values less than( -50 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 80 )
  (
    subpartition p_range_2_2 values less than( maxvalue )
  ),
  partition p_range_3 values less than( 100 ),
  partition p_range_4 values less than( 180 )
  (
    subpartition p_range_4_1 values less than(10 ),
    subpartition p_range_4_2 values less than(20 ),
    subpartition p_range_4_3 values less than(30 ),
    subpartition p_range_4_4 values less than(40 ),
    subpartition p_range_4_5 values less than(50 ),
    subpartition p_range_4_6 values less than(60 ),
    subpartition p_range_4_7 values less than(70 ),
    subpartition p_range_4_8 values less than( maxvalue )
  ),
    partition p_range_5 values less than( maxvalue )
   (
    subpartition p_range_5_1 values less than(10 ),
    subpartition p_range_5_2 values less than(20 ),
    subpartition p_range_5_3 values less than(30 ),
    subpartition p_range_5_4 values less than(40 ),
    subpartition p_range_5_5 values less than(50 ),
    subpartition p_range_5_6 values less than(60 ),
    subpartition p_range_5_7 values less than(70 ),
    subpartition p_range_5_8 values less than(80 ),
    subpartition p_range_5_9 values less than(90 ),
    subpartition p_range_5_10 values less than(1000000)
  )
);
--step3: 一级分区键创建索引; expect:成功
create unique index on t_subpartition_0307(col_1);
--step4: 二级分区键创建索引; expect:成功
create unique index on t_subpartition_0307(col_2);
--step5: 两个分区键创建索引; expect:成功
create unique index on t_subpartition_0307(col_1,col_2);
--step6: 创建索引,索引列数超过31; expect:合理报错
create unique index on t_subpartition_0307(col_1,col_2,col_3 ,col_4,col_5 ,col_6 ,col_7 ,col_8 ,col_9,col_10,col_11,col_12,col_13,col_14,col_15,col_16,col_17,col_18,col_19,col_20,col_21,col_22,col_23,col_24,col_25,col_26,col_27,col_28,col_29,col_30,col_31,col_32,col_33,col_34,col_35,col_36);
--step7: 创建索引,索引列数等于31; expect:成功
create unique index on t_subpartition_0307(col_1,col_2,col_3 ,col_4,col_5 ,col_6 ,col_7 ,col_8 ,col_9,col_10,col_11,col_12,col_13,col_14,col_15,col_16,col_17,col_18,col_19,col_20,col_21,col_22,col_23,col_24,col_25,col_26,col_27,col_28,col_29,col_30,col_31);
--step8: 插入数据; expect:成功
insert into  t_subpartition_0307 values (generate_series(-10, 90000,2),generate_series(-10, 90000,2),generate_series(-10, 90000,2));
--step9: 查看执行计划; expect:成功
explain select * from t_subpartition_0307;

--step10: 指定不同的表空间创建索引; expect:成功
create index  on t_subpartition_0307 (col_1 asc) tablespace ts_subpartition_0307_01;
--step11: 创建部分global索引; expect:合理报错
create index  on t_subpartition_0307 (col_1 asc) tablespace ts_subpartition_0307_01 where col_1 < 4;
--step12: 创建唯一部分索引; expect:成功
create unique index  on t_subpartition_0307 (col_1,col_2 asc) tablespace ts_subpartition_0307_01 where col_1 < 4;

--step13: 指定first创建索引; expect:成功
create unique index  on t_subpartition_0307 (col_1,col_2 nulls first) tablespace ts_subpartition_0307_01 where col_1 < 4;
--step14: 索引键不包含分区键创建local索引; expect:合理报错
create  unique index on t_subpartition_0307(col_1) local;
--step15: 已存在local索引,创建global索引; expect:合理报错
create unique index on t_subpartition_0307(col_1,col_2) global;
--step16: 删除local索引; expect:成功
drop index t_subpartition_0307_col_1_col_2_idx;
drop index t_subpartition_0307_col_1_col_2_idx1;
drop index t_subpartition_0307_col_1_col_2_idx2;
--step17: 不存在local索引,创建global索引; expect:成功
create unique index on t_subpartition_0307(col_1,col_2) global;

--step18: 创建二级分区表,和系统表同名; expect:成功
drop table if exists public.pg_partition cascade;
create table pg_partition
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0307
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than(-80 )
  (
    subpartition p_range_1_1 values less than(  -20),
    subpartition p_range_1_2 values less than( 50 ),
    subpartition p_range_1_3 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 80 )
  (
    subpartition p_range_2_1 values less than( 50 ),
    subpartition p_range_2_2 values less than( maxvalue )
  ),
  partition p_range_3 values less than( 100 ),
  partition p_range_4 values less than( 200 )
  (
    subpartition p_range_4_1 values less than( 30 ),
    subpartition p_range_4_2 values less than( 100),
    subpartition p_range_4_3 values less than( 150 ),
    subpartition p_range_4_4 values less than( maxvalue )
  )
);
--step19: 清空数据; expect:成功
truncate public.pg_partition;
--step20: 插入数据; expect:成功
insert into public.pg_partition values(-90,-10,3,8),(-90,10,3,8),(-100,80,3,8);
--step21: 插入数据; expect:成功
insert into public.pg_partition values(90,-10,3,8),(90,10,3,8),(100,80,3,8);
select pg_sleep(2);
--step22: 查询数据; expect:成功6
select n_tup_ins from pg_stat_user_tables where relname = 'pg_partition';

--step23: 创建普通表,和系统表同名; expect:成功
drop table if exists public.pg_class cascade;
create table pg_class
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
);
--step24: 创建一级分区表,和系统表同名; expect:成功
drop table if exists public.pg_class cascade;
create table pg_class
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
partition by range (col_1)
(
partition p_range_2 values less than( 200 ),
partition p_range_4 values less than( 400 ),
partition p_range_8 values less than( 800 )
);

--step25: 清理环境; expect:成功
drop table if exists public.pg_partition;
drop table if exists public.pg_class;
drop table if exists t_subpartition_0307;
drop tablespace if exists ts_subpartition_0307;
drop tablespace if exists ts_subpartition_0307_01;