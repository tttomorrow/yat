-- @testpoint: 清空回收站中的对象

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清除回收站; expect:回收站清除成功
purge recyclebin;

--step4: 创建表、插入数据并删除表; expect:表创建成功、数据插入成功且表删除成功
drop table if exists t_timecapsule_0006;
create table t_timecapsule_0006(a int);
insert into t_timecapsule_0006 values(1);
drop table t_timecapsule_0006;

--step5: 在回收站中统计原始对象名称t_timecapsule_0006和操作类型为drop; expect:预期结果为1
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0006' and rcyoperation = 'd';

--step6: 清除回收站; expect:回收站清除成功
purge recyclebin;
purge recyclebin;
purge recyclebin;
purge recyclebin;

--step7: 创建表、插入数据并删除表; expect:表创建成功、数据插入成功且表删除成功
drop table if exists t_timecapsule_0006;
create table t_timecapsule_0006(a int);
insert into t_timecapsule_0006 values(1);
drop table t_timecapsule_0006;

--step8: 在回收站中统计原始对象名称t_timecapsule_0006和操作类型为drop; expect:预期结果为1
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0006' and rcyoperation = 'd';

--step9: 清除回收站; expect:回收站清除成功
purge recyclebin;
purge recyclebin;
purge recyclebin;
purge recyclebin;

--step10: 创建表、插入数据并删除表; expect:表创建成功、数据插入成功且表删除成功
drop table if exists t_timecapsule_0006;
create table t_timecapsule_0006(a int);
insert into t_timecapsule_0006 values(1);
drop table t_timecapsule_0006;

--step11: 在回收站中统计原始对象名称t_timecapsule_0006和操作类型为drop; expect:预期结果为1
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0006' and rcyoperation = 'd';

--step12: 清除回收站; expect:回收站清除成功
purge recyclebin;
purge recyclebin;
purge recyclebin;

--step13: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0006 purge;
purge recyclebin;

--step14: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;