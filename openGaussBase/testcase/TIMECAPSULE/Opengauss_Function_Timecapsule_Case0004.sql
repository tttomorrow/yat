-- @testpoint: 清空回收站中的表

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清除回收站; expect:回收站清除成功
purge recyclebin;

--step4: 创建表、插入数据并删除表; expect:表创建成功、数据插入成功且表删除成功
drop table if exists t_timecapsule_0004;
create table t_timecapsule_0004(a int);
insert into t_timecapsule_0004 values(1);
drop table t_timecapsule_0004;

--step5: 创建表、插入数据并删除表; expect:表创建成功、数据插入成功且表删除成功
drop table if exists t_timecapsule_0004;
create table t_timecapsule_0004(a int);
insert into t_timecapsule_0004 values(2);
drop table t_timecapsule_0004;

--step6: 创建表、插入数据并删除表; expect:表创建成功、数据插入成功且表删除成功
drop table if exists t_timecapsule_0004;
create table t_timecapsule_0004(a int);
insert into t_timecapsule_0004 values(3);
drop table t_timecapsule_0004;

--step7: 清除表; expect:表清除成功
purge table t_timecapsule_0004;

--step8: 在回收站中统计名称t_timecapsule_0004和操作类型为drop; expect:预期结果为2
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0004' and rcyoperation = 'd';

--step9: 清除表; expect:表清除成功
purge table t_timecapsule_0004;

--step10: 在回收站中统计名称t_timecapsule_0004和操作类型为drop; expect:预期结果为1
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0004' and rcyoperation = 'd';

--step11: 执行闪回drop; expect:闪回成功
timecapsule table t_timecapsule_0004 to before drop;

--step12: 查询闪回后的表; expect:查询结果为数据3
select * from t_timecapsule_0004;

--step13: 在回收站中统计名称t_timecapsule_0004和操作类型为drop; expect:预期结果为0
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0004' and rcyoperation = 'd';

--step14: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0004 purge;
purge recyclebin;

--step15: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;