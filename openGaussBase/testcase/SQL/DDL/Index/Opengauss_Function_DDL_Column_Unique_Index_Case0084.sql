-- @testpoint: 创建列存表,修改字段约束,验证数值数据类型对主键/唯一约束/唯一索引的支持,部分step合理报错

--测试点一:创建列存普通表，字段类型为数值型，新增字段唯一约束
--step1:测试点一,创建列存表，字段类型为支持的数值类型   expect:成功
drop table if exists t_columns_unique_index_0084_01;
create table t_columns_unique_index_0084_01(
id1 smallint, id2 integer, id3 bigint, id4 decimal(10,4), id5 numeric(8,3),id6 real,
id7 double precision, id8 smallserial, id9 serial, id10 bigserial) with(orientation=column);

--step2:测试点一,修改新增字段的约束为唯一约束   expect:成功
alter table t_columns_unique_index_0084_01 add constraint const_84_1 unique(id1);
alter table t_columns_unique_index_0084_01 add constraint const_84_2 unique(id2);
alter table t_columns_unique_index_0084_01 add constraint const_84_3 unique(id3);
alter table t_columns_unique_index_0084_01 add constraint const_84_4 unique(id4);
alter table t_columns_unique_index_0084_01 add constraint const_84_5 unique(id5);
alter table t_columns_unique_index_0084_01 add constraint const_84_6 unique(id6);
alter table t_columns_unique_index_0084_01 add constraint const_84_7 unique(id7);
alter table t_columns_unique_index_0084_01 add constraint const_84_8 unique(id8);
alter table t_columns_unique_index_0084_01 add constraint const_84_9 unique(id9);
alter table t_columns_unique_index_0084_01 add constraint const_84_10 unique(id10);
alter table t_columns_unique_index_0084_01 add constraint const_84_11 unique(id1,id2,id3,id4,id5,id6,id7,id8,id9,id10);

--step3:测试点一,插入数据   expect:成功
insert into t_columns_unique_index_0084_01 values(32765,2147483647,9223372036854,123456.1223,33456.255,10.3655,123456.1234,1,1,1);

--step4:测试点一,再次插入数据   expect:失败
insert into t_columns_unique_index_0084_01 values(32765,2147483647,9223372036854,123456.1223,33456.255,10.3655,123456.1234,1,1,1);

--step5:清理环境   expect:成功
drop table t_columns_unique_index_0084_01;



--测试点二:创建列存普通表，字段类型为数值型，新增字段主键约束
--step1:测试点二,创建列存表，字段类型为支持的数值类型   expect:成功
drop table if exists t_columns_unique_index_0084_02;
create table t_columns_unique_index_0084_02(
id1 smallint, id2 integer, id3 bigint, id4 decimal(10,4), id5 numeric(8,3),id6 real,
id7 double precision, id8 smallserial, id9 serial, id10 bigserial) with(orientation=column);

--step2:测试点二,修改新增字段的约束为主键约束   expect:成功
alter table t_columns_unique_index_0084_02 add primary key(id1,id2,id3,id4,id5,id6,id7,id8,id9,id10);

--step3:测试点二,插入数据   expect:成功
insert into t_columns_unique_index_0084_02 values(32765,2147483647,9223372036854,123456.1223,33456.255,10.3655,123456.1234,1,1,1);

--step4:测试点二,再次插入数据   expect:失败
insert into t_columns_unique_index_0084_02 values(32765,2147483647,9223372036854,123456.1223,33456.255,10.3655,123456.1234,1,1,1);

--step5:测试点二,清理环境   expect:成功
drop table t_columns_unique_index_0084_02;



--测试点三:创建列存普通表，字段类型为数值型，为字段新增唯一索引
--step1:测试点三,创建列存表，字段类型为支持的数值类型   expect:成功
drop table if exists t_columns_unique_index_0084_03;
create table t_columns_unique_index_0084_03(
id1 smallint, id2 integer, id3 bigint, id4 decimal(10,4), id5 numeric(8,3),id6 real,
id7 double precision, id8 smallserial, id9 serial, id10 bigserial) with(orientation=column);

--step2:测试点三,新增唯一索引   expect:成功
create unique index i_columns_unique_index_0084_01 on t_columns_unique_index_0084_03 using btree(id1);
create unique index i_columns_unique_index_0084_02 on t_columns_unique_index_0084_03 using btree(id2);
create unique index i_columns_unique_index_0084_03 on t_columns_unique_index_0084_03 using btree(id3);
create unique index i_columns_unique_index_0084_04 on t_columns_unique_index_0084_03 using btree(id4);
create unique index i_columns_unique_index_0084_05 on t_columns_unique_index_0084_03 using btree(id5);
create unique index i_columns_unique_index_0084_06 on t_columns_unique_index_0084_03 using btree(id6);
create unique index i_columns_unique_index_0084_07 on t_columns_unique_index_0084_03 using btree(id7);
create unique index i_columns_unique_index_0084_08 on t_columns_unique_index_0084_03 using btree(id8);
create unique index i_columns_unique_index_0084_09 on t_columns_unique_index_0084_03 using btree(id9);
create unique index i_columns_unique_index_0084_10 on t_columns_unique_index_0084_03 using btree(id10);
create unique index i_columns_unique_index_0084_11 on t_columns_unique_index_0084_03 using btree(id1,id2,id3,id4,id5,id6,id7,id8,id9,id10);

--step3:测试点三,插入数据   expect:成功
insert into t_columns_unique_index_0084_03 values(32765,2147483647,9223372036854,123456.1223,33456.255,10.3655,123456.1234,1,1,1);

--step4:测试点三,再次插入数据   expect:失败
insert into t_columns_unique_index_0084_03 values(32765,2147483647,9223372036854,123456.1223,33456.255,10.3655,123456.1234,1,1,1);

--step5:测试点三,清理环境   expect:成功
drop table t_columns_unique_index_0084_03;
