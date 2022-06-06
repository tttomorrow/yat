-- @testpoint: 创建列存表,修改字段约束,验证时间日期类型对主键/唯一约束/唯一索引的支持,部分step合理报错

--测试点一:创建列存普通表，字段类型为数值型，新增字段唯一约束
--step1:测试点一,创建列存表，字段类型为支持的数值类型   expect:成功
drop table if exists t_columns_unique_index_0088_01;
create table t_columns_unique_index_0088_01(
date1 timestamp with time zone,date2 timestamp without time zone,date3 date,
date4 time without time zone,date5 time with time zone,date6 interval) with(orientation=column);

--step2:测试点一,修改新增字段的约束为唯一约束   expect:成功
alter table t_columns_unique_index_0088_01 add constraint const_88_1 unique(date1);
alter table t_columns_unique_index_0088_01 add constraint const_88_2 unique(date2);
alter table t_columns_unique_index_0088_01 add constraint const_88_3 unique(date3);
alter table t_columns_unique_index_0088_01 add constraint const_88_4 unique(date4);
alter table t_columns_unique_index_0088_01 add constraint const_88_5 unique(date5);
alter table t_columns_unique_index_0088_01 add constraint const_88_6 unique(date6);
alter table t_columns_unique_index_0088_01 add constraint const_88_7 unique(date1,date2,date3,date4,date5,date6);

--step3:测试点一,插入数据   expect:成功
insert into t_columns_unique_index_0088_01 values('2021-09-27 pst','2021-09-27',date '09-27-2021','21:21:21','21:21:21 pst',interval '2' year);

--step4:测试点一,再次插入数据   expect:失败
insert into t_columns_unique_index_0088_01 values('2021-09-27 pst','2021-09-27',date '09-27-2021','21:21:21','21:21:21 pst',interval '2' year);

--step5:清理环境   expect:成功
drop table t_columns_unique_index_0088_01;



--测试点二:创建列存普通表，字段类型为数值型，新增字段主键约束
--step1:测试点二,创建列存表，字段类型为支持的数值类型   expect:成功
drop table if exists t_columns_unique_index_0088_02;
create table t_columns_unique_index_0088_02(
date1 timestamp with time zone,date2 timestamp without time zone,date3 date,
date4 time without time zone,date5 time with time zone,date6 interval) with(orientation=column);

--step2:测试点二,修改新增字段的约束为主键约束   expect:成功
alter table t_columns_unique_index_0088_02 add primary key(date1,date2,date3,date4,date5,date6);

--step3:测试点二,插入数据   expect:成功
insert into t_columns_unique_index_0088_02 values('2021-09-27 pst','2021-09-27',date '09-27-2021','21:21:21','21:21:21 pst',interval '2' year);

--step4:测试点二,再次插入数据   expect:失败
insert into t_columns_unique_index_0088_02 values('2021-09-27 pst','2021-09-27',date '09-27-2021','21:21:21','21:21:21 pst',interval '2' year);

--step5:测试点二,清理环境   expect:成功
drop table t_columns_unique_index_0088_02;



--测试点三:创建列存普通表，字段类型为数值型，为字段新增唯一索引
--step1:测试点三,创建列存表，字段类型为支持的数值类型   expect:成功
drop table if exists t_columns_unique_index_0088_03;
create table t_columns_unique_index_0088_03(
date1 timestamp with time zone,date2 timestamp without time zone,date3 date,
date4 time without time zone,date5 time with time zone,date6 interval) with(orientation=column);

--step2:测试点三,新增唯一索引   expect:成功
create unique index i_columns_unique_index_0088_01 on t_columns_unique_index_0088_03 using btree(date1);
create unique index i_columns_unique_index_0088_02 on t_columns_unique_index_0088_03 using btree(date2);
create unique index i_columns_unique_index_0088_03 on t_columns_unique_index_0088_03 using btree(date3);
create unique index i_columns_unique_index_0088_04 on t_columns_unique_index_0088_03 using btree(date4);
create unique index i_columns_unique_index_0088_05 on t_columns_unique_index_0088_03 using btree(date5);
create unique index i_columns_unique_index_0088_06 on t_columns_unique_index_0088_03 using btree(date6);
create unique index i_columns_unique_index_0088_07 on t_columns_unique_index_0088_03 using btree(date1,date2,date3,date4,date5,date6);

--step3:测试点三,插入数据   expect:成功
insert into t_columns_unique_index_0088_03 values('2021-09-27 pst','2021-09-27',date '09-27-2021','21:21:21','21:21:21 pst',interval '2' year);

--step4:测试点三,再次插入数据   expect:失败
insert into t_columns_unique_index_0088_03 values('2021-09-27 pst','2021-09-27',date '09-27-2021','21:21:21','21:21:21 pst',interval '2' year);

--step5:测试点三,清理环境   expect:成功
drop table t_columns_unique_index_0088_03;

