-- @testpoint: 验证CSN闪回查询csn边界值,合理报错

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
drop table if exists t_timecapsule_0069;
create table t_timecapsule_0069(a int);

--step5: 边界值为2^63; expect:闪回失败
select * from t_timecapsule_0069 timecapsule csn 9223372036854775808;

--step6: 边界值为2^63-1; expect:闪回失败
select * from t_timecapsule_0069 timecapsule csn 9223372036854775807;

--step7: 边界值为0; expect:闪回失败
select * from t_timecapsule_0069 timecapsule csn 0;

--step8: 边界值为-0; expect:闪回失败
select * from t_timecapsule_0069 timecapsule csn -1;

--step9: 边界值为-2^63+1; expect:闪回失败
select * from t_timecapsule_0069 timecapsule csn -9223372036854775807;

--step10: 边界值为-2^63; expect:闪回失败
select * from t_timecapsule_0069 timecapsule csn -9223372036854775808;

--step11: 边界值为-2^63-1; expect:闪回失败
select * from t_timecapsule_0069 timecapsule csn -9223372036854775809;

--step12: 清理环境 expect:清理环境成功
drop table if exists t_timecapsule_0069;
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