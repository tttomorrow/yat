-- @testpoint: upsert子查询是否支持PBE/BYPASS/SMP验证，不符合语法要求，合理报错

--创建upeset及子查询表，插入数据
drop table if exists t_dml_upsert_sub0130_01;
create table t_dml_upsert_sub0130_01 (b int primary key,c text);
insert into t_dml_upsert_sub0130_01 select generate_series(1,100000),'c-'||generate_series(1,100000);
insert into t_dml_upsert_sub0130_01 select generate_series(100001,200000),'c-'||generate_series(100001,200000);
insert into t_dml_upsert_sub0130_01 select generate_series(200001,300000),'c-'||generate_series(200001,300000);
drop table if exists t_dml_upsert_sub0130_02;
create table t_dml_upsert_sub0130_02 (b int primary key,d text);
insert into t_dml_upsert_sub0130_02 values(generate_series(1,10000),'d-'||generate_series(1,10000));
--创建upsert表，组合主键场景
drop table if exists t_dml_upsert0130;
create table t_dml_upsert0130 (a int primary key , b text, c text, d text);
insert into t_dml_upsert0130 values (1,1,1),(2,2,2),(3,3,3),(4,4,4);
analyze t_dml_upsert_sub0130_01;
analyze t_dml_upsert_sub0130_02;
analyze t_dml_upsert0130;
select * from t_dml_upsert0130;
--PBE，不支持，合理报错
prepare cdselect(int) AS select distinct(tb1.c),tb2.d from t_dml_upsert_sub0130_01 tb1,t_dml_upsert_sub0130_02 tb2 where tb1.b =$1 and tb1.b=tb2.b limit 1 ;
execute cdselect(1);
insert into t_dml_upsert0130 values (3,3) on duplicate key update (c,d) = (execute cdselect(1));
deallocate prepare cdselect ;
prepare cdselect(int) AS select distinct(tb1.c) from t_dml_upsert_sub0130_01 tb1,t_dml_upsert_sub0130_02 tb2 where tb1.b =$1 and tb1.b=tb2.b limit 1 ;
execute cdselect(1);
insert into t_dml_upsert0130 values (3,3) on duplicate key update c = (execute cdselect(1));
deallocate prepare cdselect ;
--bypass，不支持，但不报错，没有Bypass关键字
set enable_opfusion=on;
set enable_beta_opfusion=on;
set enable_bitmapscan=off;
set enable_seqscan=off;
set opfusion_debug_mode = 'log';
set log_min_messages=debug;
set logging_module = 'on(OPFUSION)';
explain (costs off, verbose) select c from t_dml_upsert_sub0130_01 where b > 13 limit 1;
explain (costs off, verbose) insert into t_dml_upsert0130 values (3,3) on duplicate key update c = (select c from t_dml_upsert_sub0130_01 where b > 13 limit 1);
insert into t_dml_upsert0130 values (3,3) on duplicate key update c = (select c from t_dml_upsert_sub0130_01 where b > 13 limit 1);
select * from t_dml_upsert0130;
reset enable_opfusion;
reset enable_beta_opfusion;
reset enable_bitmapscan;
reset enable_seqscan;
reset opfusion_debug_mode;
reset log_min_messages;
reset logging_module;
--smp,不支持，但不报错；查询SQL，单独执行进行并行查询，在upsert语句中子查询不进行并行查询
set query_dop = 2;
explain (costs off, verbose) select count(*) from t_dml_upsert_sub0130_01;
explain (costs off, verbose) insert into t_dml_upsert0130 values (4,4,'test') on duplicate key update c = (select count(*) from t_dml_upsert_sub0130_01);
insert into t_dml_upsert0130 values (4,4,'test') on duplicate key update c = (select count(*) from t_dml_upsert_sub0130_01);
select * from t_dml_upsert0130;

--测试数据清理
drop table if exists t_dml_upsert0130;
drop table if exists t_dml_upsert_sub0130_01;
drop table if exists t_dml_upsert_sub0130_02;