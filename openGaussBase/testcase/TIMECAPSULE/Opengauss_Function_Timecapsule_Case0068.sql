-- @testpoint: 对系统表,视图及临时表执行CSN,timestamp闪回及闪回查询,合理报错

--step1: 查询参数默认值; expect:显示默认值依次为off/0/0
show enable_recyclebin;
show vacuum_defer_cleanup_age;
show version_retention_age;

--step2: 修改参数值; expect:显示结果依次为on/1000/1000
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;
alter system set vacuum_defer_cleanup_age to 1000;
select pg_sleep(2);
show vacuum_defer_cleanup_age;
alter system set version_retention_age to 1000;
select pg_sleep(2);
show version_retention_age;

--step3: 清空回收站; expect:回收站清空成功
purge recyclebin;

--step4: 创建表; expect:表创建成功
drop table if exists t_timecapsule_0068_01;
create table t_timecapsule_0068_01(a int);
select pg_sleep(4);

--step5: 对系统表执行csn闪回查询; expect:闪回失败
select * from pg_class timecapsule csn 92233720368547758;
timecapsule table pg_class to csn 92233720368547758;
select * from gs_txn_snapshot timecapsule csn 92233720368547758;
timecapsule table gs_txn_snapshot to csn 92233720368547758;

--step6: 创建视图; expect:视图创建成功
drop view if exists v_timecapsule_0068;
create view v_timecapsule_0068 as select * from t_timecapsule_0068_01;

--step7: 对视图执行csn闪回查询; expect:闪回失败
select * from v_timecapsule_0068 timecapsule csn 92233720368547758;
timecapsule table v_timecapsule_0068 to csn 92233720368547758;

--step8: 创建临时表; expect:临时表创建成功
drop  table if exists t_timecapsule_0068_02;
create temp table t_timecapsule_0068_02 as (select * from t_timecapsule_0068_01 limit 0);

--step9: 对临时表执行timestamp闪回查询; expect:闪回失败
select * from t_timecapsule_0068_02 timecapsule timestamp now();
timecapsule table t_timecapsule_0068_02 to timestamp now();

--step10: 清理环境 expect:环境清理成功
drop view  v_timecapsule_0068;
drop table if exists t_timecapsule_0068_01 purge;
drop table if exists t_timecapsule_0068_02 purge;
purge recyclebin;

--step11: 恢复默认值; expect:恢复成功，依次显示结果为off/0/0
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;
alter system set vacuum_defer_cleanup_age to 0;
select pg_sleep(2);
show vacuum_defer_cleanup_age;
alter system set version_retention_age to 0;
select pg_sleep(2);
show version_retention_age;