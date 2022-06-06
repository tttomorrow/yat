-- @testpoint: 闪回查询timestamp时间段

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
drop table if exists  t_timecapsule_0088 purge;
create table t_timecapsule_0088 (id int);

--step5: 创建索引; expect:索引创建成功
create index i_timecapsule_0088 on t_timecapsule_0088 (id);

--step6: 向表中插入数据; expect:数据插入成功
insert into t_timecapsule_0088 values(1);

--step7: 强制延迟4秒; expect:延迟成功
select pg_sleep(4);

--step8: 更新表数据; expect:表数据更新成功
update t_timecapsule_0088 set id = 2 where id = 1;

--step9: 向表中插入数据; expect:数据插入成功
insert into t_timecapsule_0088 values(10);

--step10: 查询表数据; expect:表数据查询成功
select * from t_timecapsule_0088 order by id;

--step11: 闪回查询timestamp时间段; expect:闪回成功
select * from t_timecapsule_0088 timecapsule timestamp now() - 1/(24*60*60) where id > 0 order by id;

--step12: 清理环境 expect:环境清理成功
drop table if exists t_timecapsule_0088;
purge recyclebin;

--step13: 恢复默认值; expect:恢复成功，依次显示结果为off/0/0
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;
alter system set vacuum_defer_cleanup_age to 0;
select pg_sleep(2);
show vacuum_defer_cleanup_age;
alter system set version_retention_age to 0;
select pg_sleep(2);
show version_retention_age;
