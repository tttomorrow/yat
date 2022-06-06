-- @testpoint: 子对象删除,子对象c1列默认值依赖外部对象

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 如果表存在清除表且清除回收站; expect:表清除成功且回收站清除成功
drop table if exists t_timecapsule_0024;
purge recyclebin;

--step4: 创建序列; expect:序列创建成功
create sequence seq_timecapsule_0024;

--step5: 创建表; expect:表创建成功
create table t_timecapsule_0024 (c1 int default nextval('seq_timecapsule_0024'), c2 serial);

--step6: 删除表; expect:表删除成功
drop table t_timecapsule_0024;

--step7: 从系统表中检查约束; expect:显示两条数据
select substr(rcyoriginname, 1, 9) rcyoriginname, rcyoperation, rcytype, rcycanrestore, rcycanpurge from gs_recyclebin order by rcyrelid;

--step8: 清空回收站; expect:回收站清空成功
purge recyclebin;

--step9: 删除序列; expect:删除成功
drop sequence seq_timecapsule_0024;

--step10: 从系统表中检查约束; expect:显示结果为空
select substr(rcyoriginname, 1, 9) rcyoriginname, rcyoperation, rcytype, rcycanrestore, rcycanpurge from gs_recyclebin order by rcyrelid;

--step11: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0024 purge;

--step12: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;