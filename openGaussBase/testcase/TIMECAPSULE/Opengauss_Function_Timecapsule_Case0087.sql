-- @testpoint: 分区表不支持timestamp闪回查询,合理报错

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

--step4: 创建分区表并插入数据; expect:分区表创建成功且数据插入成功
drop table if exists t_timecapsule_0087;
create table t_timecapsule_0087 (id int)
partition by range (id)
(
partition p1 values less than (10),
partition p2 values less than (20)
);
insert into t_timecapsule_0087 values(1);

--step5: 强制延迟4秒; expect:延迟成功
select pg_sleep(4);

--step6: 增加分区; expect:分区增加成功
alter table t_timecapsule_0087 add partition p3 values less than (30);

--step7: 执行timestamp闪回查询; expect:合理报错
select * from t_timecapsule_0087 timecapsule timestamp now() - 1/(24*60*60);

--step8: 清理环境 expect:环境清理成功
drop table if exists t_timecapsule_0087;
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