-- @testpoint: 逻辑删除和物理删除

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清除回收站; expect:回收站清除成功
purge recyclebin;

--step4: 创建表; expect:表创建成功
drop table if exists t_timecapsule_0002_01;
drop table if exists t_timecapsule_0002_02;
create table t_timecapsule_0002_01(a int, b int);
create table t_timecapsule_0002_02(c int, d int);

--step5: 创建视图; expect:视图创建成功
create view v_timecapsule_0002 as select * from t_timecapsule_0002_01, t_timecapsule_0002_02;

--step6: 插入数据; expect:数据插入成功
insert into t_timecapsule_0002_01 values (1),(2),(3);
insert into t_timecapsule_0002_02 values (1),(2),(3);

--step7: 删除表t_timecapsule_0002_01; expect:表删除成功
drop table t_timecapsule_0002_01 cascade;

--step8: 统计视图; expect:统计结果为0
select count(*) from pg_views where viewname = 'v_timecapsule_0002';

--step9: 在回收站中统计名称t_timecapsule_0002_01和操作类型为drop; expect:预期结果为1
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0002_01' and rcyoperation = 'd';

--step10: 删除表t_timecapsule_0002_02; expect:表删除成功
drop table t_timecapsule_0002_02 cascade;

--step11: 在回收站中统计名称t_timecapsule_0002_02和操作类型为drop; expect:预期结果为1
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0002_02' and rcyoperation = 'd';

--step12: 对表t_timecapsule_0002_01执行闪回drop; expect:闪回成功
timecapsule table t_timecapsule_0002_01 to before drop;

--step13: 查询闪回后的表数据; expect:显示3条数据与预期结果一致
select * from t_timecapsule_0002_01;

--step14: 对表t_timecapsule_0002_02执行闪回drop; expect:闪回成功
timecapsule table t_timecapsule_0002_02 to before drop;

--step15: 查询闪回后的表数据; expect:显示3条数据与预期结果一致
select * from t_timecapsule_0002_02;

--step16: 统计视图; expect:预期结果为0
select count(*) from pg_views where viewname = 'v_timecapsule_0002';

--step17: 删除表t_timecapsule_0002_01,t_timecapsule_0002_02; expect:表删除成功
drop table t_timecapsule_0002_01;
drop table t_timecapsule_0002_02;

--step18: purge清空回收站中指定表; expect:回收站中指定表成功
purge table t_timecapsule_0002_01;
purge table t_timecapsule_0002_02;

--step19: 清空回收站; expect:回收站清空成功
purge recyclebin;

--step20: 恢复默认值; expect:恢复默认值成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;