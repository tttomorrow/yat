-- @testpoint: 创建列存表,修改字段约束,验证其他类型对主键/唯一约束/唯一索引的支持,部分step合理报错

--测试点一:创建列存普通表，字段类型为数值型，新增字段唯一约束
--step1:测试点一,创建列存表，字段类型为支持的数值类型   expect:成功
drop table if exists t_columns_unique_index_0090_01;
create table t_columns_unique_index_0090_01(
salary money,name clob) with(orientation=column);

--step2:测试点一,修改新增字段的约束为唯一约束   expect:成功
alter table t_columns_unique_index_0090_01 add constraint const_90_1 unique(salary);
alter table t_columns_unique_index_0090_01 add constraint const_90_2 unique(name);
alter table t_columns_unique_index_0090_01 add constraint const_90_3 unique(salary,name);

--step3:测试点一,插入数据   expect:成功
insert into t_columns_unique_index_0090_01 values(5000.00,'hathyweii');

--step4:测试点一,再次插入数据   expect:失败
insert into t_columns_unique_index_0090_01 values(5000.00,'hathyweii');

--step5:清理环境   expect:成功
drop table t_columns_unique_index_0090_01;



--测试点二:创建列存普通表，字段类型为数值型，新增字段主键约束
--step1:测试点二,创建列存表，字段类型为支持的数值类型   expect:成功
drop table if exists t_columns_unique_index_0090_02;
create table t_columns_unique_index_0090_02(
salary money,name clob) with(orientation=column);

--step2:测试点二,修改新增字段的约束为主键约束   expect:成功
alter table t_columns_unique_index_0090_02 add primary key(salary,name);

--step3:测试点二,插入数据   expect:成功
insert into t_columns_unique_index_0090_02 values(5000.00,'hathyweii');

--step4:测试点二,再次插入数据   expect:失败
insert into t_columns_unique_index_0090_02 values(5000.00,'hathyweii');

--step5:测试点二,清理环境   expect:成功
drop table t_columns_unique_index_0090_02;



--测试点三:创建列存普通表，字段类型为数值型，为字段新增唯一索引
--step1:测试点三,创建列存表，字段类型为支持的数值类型   expect:成功
drop table if exists t_columns_unique_index_0090_03;
create table t_columns_unique_index_0090_03(
salary money,name clob) with(orientation=column);

--step2:测试点三,新增唯一索引   expect:成功
create unique index i_columns_unique_index_0090_01 on t_columns_unique_index_0090_03 using btree(salary);
create unique index i_columns_unique_index_0090_02 on t_columns_unique_index_0090_03 using btree(name);
create unique index i_columns_unique_index_0090_03 on t_columns_unique_index_0090_03 using btree(salary,name);

--step3:测试点三,插入数据   expect:成功
insert into t_columns_unique_index_0090_03 values(5000.00,'hathyweii');

--step4:测试点三,再次插入数据   expect:失败
insert into t_columns_unique_index_0090_03 values(5000.00,'hathyweii');

--step5:测试点三,清理环境   expect:成功
drop table t_columns_unique_index_0090_03;

