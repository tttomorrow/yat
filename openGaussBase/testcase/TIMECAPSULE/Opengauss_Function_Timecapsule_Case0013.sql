-- @testpoint: 闪回truncate和drop结合,drop表后执行truncate闪回合理报错,drop闪回成功

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清除回收站; expect:回收站清除成功
purge recyclebin;

--step4: 创建表、插入数据并truncate表; expect:表创建成功、数据插入成功且表清空成功
drop table if exists t_timecapsule_0013;
create table t_timecapsule_0013(a int);
insert into t_timecapsule_0013 values(1);
truncate table t_timecapsule_0013;

--step5: 在回收站中统计原始对象名称t_timecapsule_0013; expect:预期结果为1
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0013';

--step6: 删除表; expect:表删除成功
drop table t_timecapsule_0013;

--step7: 在回收站中统计原始对象名称t_timecapsule_0013; expect:预期结果为2
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0013';

--step8: 执行闪回truncate; expect:闪回失败，合理报错
timecapsule table t_timecapsule_0013 to before truncate;

--step9: 执行闪回drop; expect:闪回成功
timecapsule table t_timecapsule_0013 to before drop;

--step10: 在回收站中统计原始对象名称t_timecapsule_0013; expect:预期结果为1
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0013' ;

--step11: 查询闪回后的表; expect:查询结果为空与预期结果一致
select * from t_timecapsule_0013 order by a;

--step12: 执行闪回truncate; expect:闪回成功
timecapsule table t_timecapsule_0013 to before truncate;

--step13: 在回收站中统计原始对象名称t_timecapsule_0013; expect:预期结果为1
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0013' ;

--step14: 查询闪回后的表; expect:显示值为1与预期结果一致
select * from t_timecapsule_0013 order by a;

--step15: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0013 purge;
purge recyclebin;

--step16: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;