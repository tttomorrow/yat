-- @testpoint: range_list和hash_range二级分区表时间类型测试,部分测试点合理报错

--test1: range_list二级分区表
--step1: 创建表空间和range_list二级分区表，分区键为时间类型; expect:成功
drop table if exists t_subpartition_0009_01 cascade;
drop tablespace if exists ts_subpartition_0009 ;
create tablespace ts_subpartition_0009 relative location 'subpartition_tablespace/subpartition_tablespace_1';
create table if not exists t_subpartition_0009_01
(
    col_1 smallint,
    col_2 integer,
    col_3 bigint,
    col_4 decimal,
    col_5 numeric,
    col_6 real,
    col_7 double precision,
    col_8 character varying(10),
    col_10 varchar(10),
    col_11 character(10),
    col_12 char(10),
    col_13 character,
    col_14 char,
    col_15 text,
    col_16 nvarchar2,
    col_17 name,
    col_18 timestamp without time zone,
    col_19 timestamp with time zone,
    col_20 date
)tablespace ts_subpartition_0009
partition by range (col_18) subpartition by list ( col_19)
(
  partition p_range_1 values less than( to_date('2019-11-01','yyyy-mm-dd') )
  (
    subpartition p_list_1_1 values (to_date( '2018-11-01','yyyy-mm-dd')),
    subpartition p_list_1_2   values ( default )
  ),
  partition p_range_2 values less than(to_date('2020-11-01','yyyy-mm-dd') )
  (
    subpartition p_list_2_1 values ( to_date( '2018-11-01','yyyy-mm-dd')),
    subpartition p_list_2_2 values ( default )
  ),
  partition p_range_3 values less than( to_date('2021-11-01','yyyy-mm-dd') )
   (
    subpartition p_list_3_1 values ( default )
  ),
  partition p_range_4 values less than( to_date('2022-11-01','yyyy-mm-dd'))
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step2: split切割二级分区表分区; expect:成功
alter table t_subpartition_0009_01 split subpartition p_list_2_2  values('2018-11-02')  into (subpartition add_p_01 ,subpartition add_p_02);
--step3: 插入数据; expect:成功
insert into t_subpartition_0009_01(col_18,col_19)  values ('2019-11-01','2018-11-02');
--step4: 查询被切割的分区数据; expect:合理报错
select * from t_subpartition_0009_01 subpartition(p_list_2_2);
--step5: split切割二级分区表分区; expect:成功
alter table t_subpartition_0009_01 split subpartition add_p_02  values('2018-11-03','2018-11-05')  into (subpartition add_p_03 ,subpartition add_p_04);
--step6: 插入不同分区数据; expect:成功
insert into t_subpartition_0009_01(col_18,col_19)  values ('2019-11-01','2018-11-03');
insert into t_subpartition_0009_01(col_18,col_19)  values ('2019-11-01','2018-11-04');
insert into t_subpartition_0009_01(col_18,col_19)  values ('2019-11-01','2018-11-05');

--test2: hash_range二级分区表
--step7: 创建hash_range二级分区表，二级分区键为时间类型; expect:成功
drop table if exists t_subpartition_0009_02;
create table t_subpartition_0009_02
(
    col_1 int ,
    col_2 int  ,
    col_3 int  not null ,
    col_4 int,
    col_19 timestamp with time zone
)
tablespace ts_subpartition_0009
partition by hash (col_3) subpartition by range (col_19)
(  partition p_hash_1
  (
    subpartition p_range_1_1 values less than( to_date('2024-11-01','yyyy-mm-dd') ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_hash_2
  (
    subpartition p_range_2_1 values less than( to_date('2018-11-01','yyyy-mm-dd') ),
    subpartition p_range_2_2 values less than( to_date('2019-11-01','yyyy-mm-dd') ),
    subpartition p_range_2_3 values less than( to_date('2020-11-01','yyyy-mm-dd') ),
    subpartition p_range_2_4 values less than( to_date('2021-11-01','yyyy-mm-dd') ),
    subpartition p_range_2_5 values less than( to_date('2022-11-01','yyyy-mm-dd') ),
    subpartition p_range_2_6 values less than( to_date('2023-11-01','yyyy-mm-dd') ),
    subpartition p_range_2_7 values less than( maxvalue )
  ),
    partition p_hash_3
  (
    subpartition p_range_3_1 values less than( to_date('2024-11-01','yyyy-mm-dd') ),
    subpartition p_range_3_2 values less than( to_date('2025-11-01','yyyy-mm-dd') ),
    subpartition p_range_3_3 values less than( to_date('2026-11-01','yyyy-mm-dd') ),
    subpartition p_range_3_4 values less than( maxvalue )
  ),
    partition p_hash_4,
    partition p_hash_5
    (
    subpartition p_range_5_1 values less than( maxvalue )
    ),
    partition p_hash_7
) enable row movement;
--step8: split切割二级分区表分区; expect:成功
alter table t_subpartition_0009_02 split subpartition p_range_3_3  at('2026-10-03')  into (subpartition add_p_01 ,subpartition add_p_02);
alter table t_subpartition_0009_02 split subpartition p_range_3_4  at('2027-10-03')  into (subpartition add_p_03 ,subpartition add_p_04);
--step9: 插入不同分区数据; expect:成功
insert into t_subpartition_0009_02(col_3,col_19)  values (22,'2026-10-03');
insert into t_subpartition_0009_02(col_3,col_19)  values (22,'2026-10-02');
insert into t_subpartition_0009_02(col_3,col_19)  values (22,'2026-10-04');
insert into t_subpartition_0009_02(col_3,col_19)  values (22,'2027-10-03');
insert into t_subpartition_0009_02(col_3,col_19)  values (22,'2027-10-02');
insert into t_subpartition_0009_02(col_3,col_19)  values (22,'2027-10-04');

--step10: 删除表; expect:成功
drop table if exists t_subpartition_0009_01 cascade;
drop table if exists t_subpartition_0009_02 cascade;
drop tablespace if exists ts_subpartition_0009 ;