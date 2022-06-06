-- @testpoint: 重复truncate清空同一张表

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清除回收站; expect:回收站清除成功
purge recyclebin;

--step4: 创建表、插入数据并truncate表; expect:表创建成功、数据插入成功且表清空成功
drop table if exists t_timecapsule_0012;
create table t_timecapsule_0012(a int);
insert into t_timecapsule_0012 values(1);
truncate table t_timecapsule_0012;

--step5: 在回收站中统计原始对象名称t_timecapsule_0012和操作类型为truncate; expect:预期结果为1
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0012' and rcyoperation = 't';

--step6: 向插入数据并清空表; expect:数据插入成功且表清空成功
insert into t_timecapsule_0012 values(2);
truncate table t_timecapsule_0012;

--step7: 在回收站中统计名称t_timecapsule_0012和操作类型为truncate; expect:预期结果为2
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0012' and rcyoperation = 't';

--step8: 向表插入数据并清空表; expect:数据插入成功且表删除成功
insert into t_timecapsule_0012 values(3);
truncate table t_timecapsule_0012;

--step9: 在回收站中统计名称t_timecapsule_0012和操作类型为truncate; expect:预期结果为3
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0012' and rcyoperation = 't';

--step10: 执行闪回truncate; expect:闪回成功
timecapsule table t_timecapsule_0012 to before truncate;

--step11: 在回收站中统计名称t_timecapsule_0012和操作类型为truncate; expect:预期结果为3
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0012' and rcyoperation = 't';

--step12: 查询闪回后的表; expect:显示值为1与预期结果一致
select * from t_timecapsule_0012 order by a;

--step13: 执行闪回truncate; expect:闪回成功
timecapsule table t_timecapsule_0012 to before truncate;

--step14: 查询闪回后的表; expect:显示值为2与预期结果一致
select * from t_timecapsule_0012 order by a;

--step15: 执行闪回truncate; expect:闪回成功
timecapsule table t_timecapsule_0012 to before truncate;

--step16: 查询闪回后的表; expect:显示值为3与预期结果一致
select * from t_timecapsule_0012 order by a;

--step17: 执行闪回truncate; expect:闪回成功
timecapsule table t_timecapsule_0012 to before truncate;

--step18: 查询闪回后的表; expect:查询结果为空
select * from t_timecapsule_0012 order by a;

--step19: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0012 purge;
purge recyclebin;

--step20: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;