-- @testpoint: 验证无效csn值,合理报错

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
drop table if exists t_timecapsule_0084;
create table t_timecapsule_0084 (id int);
insert into t_timecapsule_0084 values(1);

--step5: 查询表数据; expect:成功显示插入的数据
select * from t_timecapsule_0084;

--step6: csn闪回查询无效csn; expect:合理报错
select * from t_timecapsule_0084 timecapsule csn 0;
select * from t_timecapsule_0084 timecapsule csn 1;
select * from t_timecapsule_0084 timecapsule csn 9999999999999999;
select * from t_timecapsule_0084 timecapsule csn 9999999999999998 + 1/1;
select * from t_timecapsule_0084 timecapsule csn 'asdfgag';
select * from t_timecapsule_0084 timecapsule csn (select next_csn from gs_get_next_xid_csn());
select * from t_timecapsule_0084 timecapsule csn -1;

--step7: 清理环境 expect:环境清理成功
drop table if exists t_timecapsule_0084;
purge recyclebin;

--step8: 恢复默认值; expect:恢复成功，依次显示结果为off/0/0
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;
alter system set vacuum_defer_cleanup_age to 0;
select pg_sleep(2);
show vacuum_defer_cleanup_age;
alter system set version_retention_age to 0;
select pg_sleep(2);
show version_retention_age;