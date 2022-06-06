-- @testpoint: 列存普通表创建唯一索引，添加新的字段，step5合理报错

--测试点一:列存普通表,增加新的字段后,创建唯一索引,插入数据
--step1:测试点一,创建列存普通表   expect:成功
drop table if exists t_columns_unique_index_0064_01;
create table t_columns_unique_index_0064_01(id1 int,id2 int) with(orientation=column);

--step2:测试点一,增加新的字段   expect:成功
alter table t_columns_unique_index_0064_01 add id3 int;

--step3:测试点一,向新增的字段添加唯一索引   expect:成功
create unique index i_columns_unique_index_0064_01 on t_columns_unique_index_0064_01 using btree(id3);

--step4:测试点一,向表中插入数据   expect:成功
insert into t_columns_unique_index_0064_01 values(generate_series(1,100),generate_series(1,100),generate_series(1,100));

--step5:测试点一,再次向表中插入数据   expect:插入失败
insert into t_columns_unique_index_0064_01 values(generate_series(1,100),generate_series(1,100),generate_series(1,100));

--step6:测试点一,查看数据   expect:成功
select count(*) from t_columns_unique_index_0064_01;

--step7:测试点一,清理环境   expect:成功
drop table t_columns_unique_index_0064_01 cascade;



--测试点二:创建唯一索引后,增加新的字段,插入数据
--step1:测试点二,创建列存普通表   expect:成功
drop table if exists t_columns_unique_index_0064_02;
create table t_columns_unique_index_0064_02(id1 int,id2 int) with(orientation=column);

--step2:测试点二,创建唯一索引   expect:成功
create unique index i_columns_unique_index_0064_02 on t_columns_unique_index_0064_02 using btree(id1,id2);

--step3:测试点二,增加新的字段   expect:成功
alter table t_columns_unique_index_0064_02 add(id3 int,id4 int,id5 int);

--step4:测试点二,插入数据   expect:成功
insert into t_columns_unique_index_0064_02 values(generate_series(1,100),generate_series(1,100),generate_series(1,100),generate_series(1,100),generate_series(1,100));

--step5:测试点二,查看数据   expect:成功
select count(*) from t_columns_unique_index_0064_02;

--step6:测试点二,清理环境   expect:成功
drop table t_columns_unique_index_0064_02 cascade;



--测试点三:增加新的字段指定唯一约束or索引,插入数据
--step1:测试点三,创建列存普通表   expect:成功
drop table if exists t_columns_unique_index_0064_03;
create table t_columns_unique_index_0064_03(id1 int,id2 int) with(orientation=column);

--step2:测试点三,增加新的字段,指定主键约束   expect:成功
alter table t_columns_unique_index_0064_03 add id3 int primary key;

--step3:测试点三,增加新的字段,指定唯一约束   expect:成功
alter table t_columns_unique_index_0064_03 add id4 int unique;

--step4:测试点三,插入数据   expect:成功
insert into t_columns_unique_index_0064_03 values(generate_series(1,100),generate_series(1,100),generate_series(1,100),generate_series(1,100));

--step5:测试点三,查看数据   expect:成功
select count(*) from t_columns_unique_index_0064_03;

--step6:测试点三,清理环境   expect:成功
drop table t_columns_unique_index_0064_03 cascade;

