-- @testpoint: 基表依赖外部模式的子对象删除,合理报错

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清除回收站; expect:回收站清除成功
drop table if exists t_timecapsule_008;
purge recyclebin;

--step4: 创建模式; expect:模式创建成功
create schema s_timecapsule_0018;

--step5: 基于模式创建表; expect:表创建成功
create table s_timecapsule_0018.t_timecapsule_0018(col1 int);

--step6: 删除模式下的表; expect:表删除成功
drop table s_timecapsule_0018.t_timecapsule_0018;

--step7: 删除模式; expect:模式删除失败合理报错
drop schema s_timecapsule_0018;

--step8: 删除该模式下的所有东西; expect:删除失败合理报错
drop schema s_timecapsule_0018 cascade;

--step9: 清空回收站中该模式下的表; expect:回收站中该模式下的表清空成功
purge table s_timecapsule_0018.t_timecapsule_0018;

--step10: 删除模式; expect:模式删除成功
drop schema s_timecapsule_0018;

--step11: 在回收站中截取原始对象名称; expect:截取结果为空
select substr(rcyoriginname, 1, 9) rcyoriginname, rcyoperation, rcytype, rcycanrestore, rcycanpurge from gs_recyclebin order by rcyrelid;

--step12: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0018 purge;
drop schema if exists s_timecapsule_0018;
purge recyclebin;

--step13: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;