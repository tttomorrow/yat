-- @testpoint: 二级分区表：分区键类型,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0209;
drop tablespace if exists ts_subpartition_0209;
create tablespace ts_subpartition_0209 relative location 'subpartition_tablespace/subpartition_tablespace_0209';

--test1: 分区键类型--range,range分区分区键支持smallint、integer、bigint、decimal、numeric、real、double precision、character varying(n)、varchar(n)、character(n)、char(n)、character、char、text、nvarchar2、name、timestamp[(p)] [without timezone]、timestamp[(p)] [with time zone]、date
--step2: 创建二级分区表，指定不同类型的分区键; expect:成功
create   table if not exists t_subpartition_0209
(   col_1 smallint	,
    col_2 integer	,
    col_3 bigint	,
    col_4 decimal	,
    col_5 numeric	,
    col_6 real	,
    col_7 double precision	,
    col_8 character varying(10)	,
    col_10 varchar(10)	,
    col_11 character(10)	,
    col_12 char(10)	,
    col_13 character,
    col_14 char	,
    col_15 text	,
    col_16 nvarchar2	,
    col_17 name	,
    col_18 timestamp without time zone	,
    col_19 timestamp with time zone	,
    col_20 date
)tablespace ts_subpartition_0209
partition by range (col_12) subpartition by list ( col_13)
(
  partition p_range_1 values less than( 1)
  (
    subpartition p_list_1_1 values ( '1','2','3','4','5'),
    subpartition t_subpartition_0209   values ( default )
  ),
  partition p_range_2 values less than( 5 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than(8 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 9 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 创建二级分区表，指定不同类型的分区键; expect:合理报错
drop table if exists t_subpartition_0209;
create   table if not exists t_subpartition_0209
(   col_1 smallint	,
    col_2 integer	,
    col_3 bigint	,
    col_4 decimal	,
    col_5 numeric	,
    col_6 real	,
    col_7 double precision	,
    col_8 character varying(10)	,
    col_10 varchar(10)	,
    col_11 character(10)	,
    col_12 char(10)	,
    col_13 character,
    col_14 char	,
    col_15 text	,
    col_16 nvarchar2	,
    col_17 name	,
    col_18 timestamp without time zone	,
    col_19 timestamp with time zone	,
    col_20 date
)tablespace ts_subpartition_0209
partition by range (col_14) subpartition by list ( col_15)
(
  partition p_range_1 values less than( 1 )
  (
    subpartition p_list_1_1 values ( '1','2','3','4','5'),
    subpartition t_subpartition_0209   values ( default )
  ),
  partition p_range_2 values less than( 2 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 3 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 4 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step4: 创建二级分区表，指定不同类型的分区键; expect:成功
drop table if exists t_subpartition_0209;
create   table if not exists t_subpartition_0209
(   col_1 smallint	,
    col_2 integer	,
    col_3 bigint	,
    col_4 decimal	,
    col_5 numeric	,
    col_6 real	,
    col_7 double precision	,
    col_8 character varying(10)	,
    col_10 varchar(10)	,
    col_11 character(10)	,
    col_12 char(10)	,
    col_13 character,
    col_14 char	,
    col_15 text	,
    col_16 nvarchar2	,
    col_17 name	,
    col_18 timestamp without time zone	,
    col_19 timestamp with time zone	,
    col_20 date
)tablespace ts_subpartition_0209
partition by range (col_18) subpartition by list ( col_19)
(
  partition p_range_1 values less than( to_date('2019-11-01','yyyy-mm-dd') )
  (
    subpartition p_list_1_1 values (to_date( '2018-11-01','yyyy-mm-dd')),
    subpartition t_subpartition_0209   values ( default )
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
--step5: 创建二级分区表，指定不同类型的分区键; expect:成功
drop table if exists t_subpartition_0209;
create   table if not exists t_subpartition_0209
(   col_1 smallint	,
    col_2 integer	,
    col_3 bigint	,
    col_4 decimal	,
    col_5 numeric	,
    col_6 real	,
    col_7 double precision	,
    col_8 character varying(10)	,
    col_10 varchar(10)	,
    col_11 character(10)	,
    col_12 char(10)	,
    col_13 character,
    col_14 char	,
    col_15 text	,
    col_16 nvarchar2	,
    col_17 name	,
    col_18 timestamp without time zone	,
    col_19 timestamp with time zone	,
    col_20 date
)tablespace ts_subpartition_0209
partition by range (col_20) subpartition by list ( col_19)
(
  partition p_range_1 values less than( to_date('2019-11-01','yyyy-mm-dd') )
  (
    subpartition p_list_1_1 values (to_date( '2018-11-01','yyyy-mm-dd')),
    subpartition t_subpartition_0209   values ( default )
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

--test2: 分区键类型--list,list分区分区键支持int1、int2、int4、int8、numeric、varchar(n)、char、bpchar、nvarchar2、timestamp[(p)] [withouttime zone]、timestamp[(p)] [with time zone]、date
--step6: 创建二级分区表，指定不同类型的分区键; expect:成功
drop table if exists t_subpartition_0209;
create   table if not exists t_subpartition_0209
(
    col_1 int1	,
    col_2 int2	,
    col_3 int4	,
    col_4 int8	,
    col_5 numeric	,
    col_6 varchar(10)	,
    col_7 char	,
    col_8 bpchar	,
    col_9 nvarchar2	,
    col_10 timestamp without time zone	,
    col_11 timestamp(0) with time zone	,
    col_12 date	,
    col_13 character

)
partition by list (col_9) subpartition by list (col_13)
(
  partition p_list_1 values(default)
  (
    subpartition p_list_1_2 values ( default )
  ),
  partition p_list_2 values(11,12)
  (
    subpartition p_list_2_2 values ( default )
  )
);
--step7: 创建二级分区表，指定不同类型的分区键; expect:成功
drop table if exists t_subpartition_0209;
create   table if not exists t_subpartition_0209
(
    col_1 int1	,
    col_2 int2	,
    col_3 int4	,
    col_4 int8	,
    col_5 numeric	,
    col_6 varchar(10)	,
    col_7 char	,
    col_8 bpchar	,
    col_9 nvarchar2	,
    col_10 timestamp without time zone	,
    col_11 timestamp(0) with time zone	,
    col_12 date	,
    col_13 character,
    col_14 decimal
)
partition by list (col_13)
(
  partition p_list_1 values(default)
);

--test3: 分区键类型--hash,hash分区分区键支持int1、int2、int4、int8、numeric、varchar(n)、char、bpchar、text、nvarchar2、timestamp[(p)][without time zone]、timestamp[(p)] [with time zone]、date。
--step8: 创建二级分区表，指定不同类型的分区键; expect:成功
drop table if exists t_subpartition_0209;
create   table if not exists t_subpartition_0209
(
    col_1 int1	,
    col_2 int2	,
    col_3 int4	,
    col_4 int8	,
    col_5 numeric	,
    col_6 varchar(10)	,
    col_7 char	,
    col_8 bpchar	,
    col_9 text	,
    col_10 nvarchar2	,
    col_11 timestamp(0) without time zone	,
    col_12 timestamp(0) with time zone	,
    col_13 date
)
partition by hash (col_12) subpartition by hash (col_13)
(
  partition p_hash_1 
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 
  ),
  partition p_hash_2 
  (
    subpartition p_hash_2_1 ,
    subpartition p_hash_2_2 
  )
);

--step9: 清理环境; expect:成功
drop table if exists t_subpartition_0209;
drop tablespace if exists ts_subpartition_0209;