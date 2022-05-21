-- @testpoint: DDL闪回无效,合理报错

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

--step4: 创建表并向表中插入数据; expect:表创建成功且数据创建成功
drop table if exists t_timecapsule_0086;
create table t_timecapsule_0086 (id int);
insert into t_timecapsule_0086 values(1);

--step5: 强制延迟4秒; expect:延迟成功
select pg_sleep(4);

--step6: 创建索引并删除索引; expect:创建删除成功
create index i_timecapsule_0086 on t_timecapsule_0086 (id);
drop index i_timecapsule_0086;

--step7: 执行ddl闪回查询时间点; expect:ddl闪回无效
select * from t_timecapsule_0086 timecapsule timestamp now() - 1/(24*60*60) order by id;

--step8: 清理环境 expect:环境清理成功
drop table if exists t_timecapsule_0086;
purge recyclebin;

--step9: 恢复默认值; expect:恢复成功，依次显示结果为off/0/0
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;
alter system set vacuum_defer_cleanup_age to 0;
select pg_sleep(2);
show vacuum_defer_cleanup_age;
alter system set version_retention_age to 0;
select pg_sleep(2);
show version_retention_age;