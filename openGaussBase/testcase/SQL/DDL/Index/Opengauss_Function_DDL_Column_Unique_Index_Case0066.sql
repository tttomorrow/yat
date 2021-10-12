-- @testpoint: 列存普通表创建唯一索引，修改原有字段类型

--测试点一:列存普通表,修改原有字段类型后,创建唯一索引,插入数据
--step1:测试点一,创建列存普通表   expect:成功
drop table if exists t_columns_unique_index_0066_01;
create table t_columns_unique_index_0066_01(id1 int,id2 int,id3 int) with(orientation=column);

--step2:测试点一,修改原有字段类型   expect:成功
alter table t_columns_unique_index_0066_01 modify (id3 numeric);

--step3:测试点一,添加唯一索引   expect:成功
create unique index i_columns_unique_index_0066_01 on t_columns_unique_index_0066_01 using btree(id1,id2,id3);

--step4:测试点一,插入数据   expect:成功
insert into t_columns_unique_index_0066_01 values(generate_series(1,100),generate_series(1,100),generate_series(1,100));

--step5:测试点一,查看数据   expect:成功
select count(*) from t_columns_unique_index_0066_01;

--step6:测试点一,清理环境   expect:成功
drop table t_columns_unique_index_0066_01 cascade;


--测试点二:列存普通表,创建唯一索引后,修改原有字段类型,插入数据
--step1:测试点二,创建列存普通表   expect:成功
drop table if exists t_columns_unique_index_0066_02;
create table t_columns_unique_index_0066_02(id1 int,id2 int) with(orientation=column);

--step2:测试点二,创建唯一索引   expect:成功
create unique index i_columns_unique_index_0066_02 on t_columns_unique_index_0066_02 using btree(id1,id2);

--step3:测试点二,修改原有字段类型   expect:成功
alter table t_columns_unique_index_0066_02 modify (id2 bool);

--step4:测试点二,插入数据   expect:成功
insert into t_columns_unique_index_0066_02 values(1,0),(0,1),(1,1),(0,0);

--step5:测试点二,查看数据   expect:成功
select * from t_columns_unique_index_0066_02;

--step6:测试点二,清理环境   expect:成功
drop table t_columns_unique_index_0066_02 cascade;


--测试点三:列存普通表,创建唯一索引后,重命名原有字段,插入数据
--step1:测试点三,创建列存普通表   expect:成功
drop table if exists t_columns_unique_index_0066_03;
create table t_columns_unique_index_0066_03(id1 int,id2 int) with(orientation=column);

--step2:测试点三,创建唯一索引   expect:成功
create unique index i_columns_unique_index_0066_03 on t_columns_unique_index_0066_03 using btree(id1,id2);

--step3:测试点三,重命名原有字段   expect:成功
alter table t_columns_unique_index_0066_03 rename id2 to new_id2;

--step4:测试点三,查看字段重命名   expect:成功
select attname from pg_attribute where attrelid = (select oid from pg_class where relname='t_columns_unique_index_0066_03') and attname like 'new_id2';

--step5:测试点三,插入数据   expect:成功
insert into t_columns_unique_index_0066_03 values(1,0),(0,1),(1,1),(0,0);

--step6:测试点三,查看数据   expect:成功
select * from t_columns_unique_index_0066_03;

--step7:测试点三,清理环境   expect:成功
drop table t_columns_unique_index_0066_03 cascade;
