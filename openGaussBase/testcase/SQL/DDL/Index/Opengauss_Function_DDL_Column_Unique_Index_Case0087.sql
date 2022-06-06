-- @testpoint: 创建列存表,验证时间日期类型对主键/唯一约束/唯一索引的支持,部分step合理报错

--测试点一:创建列存普通表，字段类型为时间日期类型，指定主键约束
--step1:测试点一,创建列存普通表,字段类型为时间日期类型,指定主键约束   expect:成功
drop table if exists t_columns_unique_index_0087_01;
create table t_columns_unique_index_0087_01(
date1 timestamp with time zone,date2 timestamp without time zone,date3 date,
date4 time without time zone,date5 time with time zone,date6 interval,
primary key(date1,date2,date3,date4,date5,date6)) with(orientation=column);

--step2:测试点一,插入数据   expect:成功
insert into t_columns_unique_index_0087_01 values('2021-09-27 pst','2021-09-27',date '09-27-2021','21:21:21','21:21:21 pst',interval '2' year);

--step3:测试点一,再次插入重复数据   expect:失败
insert into t_columns_unique_index_0087_01 values('2021-09-27 pst','2021-09-27',date '09-27-2021','21:21:21','21:21:21 pst',interval '2' year);

--step4:测试点一,清理环境    expect:成功
drop table t_columns_unique_index_0087_01;


--测试点二:创建列存普通表，字段类型为时间日期类型，指定唯一约束
--step1:测试点二,创建列存普通表,字段类型为时间日期类型,指定唯一约束   expect:成功
drop table if exists t_columns_unique_index_0087_02;
create table t_columns_unique_index_0087_02(
date1 timestamp with time zone,date2 timestamp without time zone,date3 date,
date4 time without time zone,date5 time with time zone,date6 interval,
constraint const_87 unique(date1,date2,date3,date4,date5)) with(orientation=column);

--step2:测试点二,插入数据   expect:成功
insert into t_columns_unique_index_0087_02 values('2021-09-27 pst','2021-09-27',date '09-27-2021','21:21:21','21:21:21 pst',interval '2' year);

--step3:测试点二,再次插入重复数据   expect:失败
insert into t_columns_unique_index_0087_02 values('2021-09-27 pst','2021-09-27',date '09-27-2021','21:21:21','21:21:21 pst',interval '2' year);

--step4:测试点二,清理环境    expect:成功
drop table t_columns_unique_index_0087_02;


--测试点三:创建列存普通表，字段类型为时间日期类型，创建唯一索引
--step1:测试点三,创建列存普通表,字段类型为时间日期类型   expect:成功
drop table if exists t_columns_unique_index_0087_03;
create table t_columns_unique_index_0087_03(
date1 timestamp with time zone,date2 timestamp without time zone,date3 date,
date4 time without time zone,date5 time with time zone,date6 interval) with(orientation=column);

--step2:创建唯一索引   expect:成功
create unique index i_columns_unique_index_0087 on t_columns_unique_index_0087_03 using btree(date1,date2,date3,date4,date5);

--step2:测试点三,插入数据   expect:成功
insert into t_columns_unique_index_0087_03 values('2021-09-27 pst','2021-09-27',date '09-27-2021','21:21:21','21:21:21 pst',interval '2' year);

--step3:测试点三,再次插入重复数据   expect:失败
insert into t_columns_unique_index_0087_03 values('2021-09-27 pst','2021-09-27',date '09-27-2021','21:21:21','21:21:21 pst',interval '2' year);

--step4:测试点三,清理环境    expect:成功
drop table t_columns_unique_index_0087_03;



