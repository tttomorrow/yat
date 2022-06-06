-- @testpoint: 清空表数据后执行闪回

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清除回收站; expect:回收站清除成功
purge recyclebin;

--step4: 清除回收站; expect:回收站清除成功
drop table if exists t_timecapsule_0003;
create table t_timecapsule_0003 (a int);
insert into t_timecapsule_0003 values(1);
insert into t_timecapsule_0003 values(2);
insert into t_timecapsule_0003 values(3);

--step5: 清空表数据; expect:表数据清空成功
truncate table t_timecapsule_0003;

--step6: 在回收站中统计名称t_timecapsule_0003和操作类型为truncate; expect:预期结果为1
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0003' and rcyoperation = 't';

--step7: 执行闪回truncate; expect:闪回成功
timecapsule table t_timecapsule_0003 to before truncate;

--step8: 查询闪回后的表; expect:查询结果为3条数据与预期结果一致
select * from t_timecapsule_0003;

--step9: 清空回收站; expect:回收站清空成功
purge recyclebin;

--step10: 用purge清除表; expect:清除成功
truncate table t_timecapsule_0003 purge;

--step11: 在回收站中统计名称t_timecapsule_0003和操作类型为truncate; expect:预期结果为0
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0003' and rcyoperation = 't';

--step12: 不放入回收站直接删除表; expect:表删除成功
drop table if exists t_timecapsule_0003 purge;

--step13: 清空回收站; expect:回收站清空成功
purge recyclebin;

--step14: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;