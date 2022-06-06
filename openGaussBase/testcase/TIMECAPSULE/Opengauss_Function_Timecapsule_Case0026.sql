-- @testpoint: 关闭回收站后执行闪回,合理报错

--step1: 查询enable_recyclebin 默认值; expect:显示默认值
show enable_recyclebin;

--step2: 修改enable_recyclebin为off; expect:显示值为off
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清除回收站; expect:回收站清除成功
drop table if exists t_timecapsule_0026;
purge recyclebin;

--step4: 创建表、插入数据并删除表; expect:表创建成功、数据插入成功且表删除成功
create table t_timecapsule_0026(a int);
insert into t_timecapsule_0026 values(1);
insert into t_timecapsule_0026 values(2);
insert into t_timecapsule_0026 values(3);
drop table t_timecapsule_0026;

--step5: 在回收站中统计原始对象名称t_timecapsule_0026和操作类型为drop; expect:预期结果为0
select count(*) from gs_recyclebin where rcyoriginname = 'tab1' and rcyoperation = 'd';

--step6: 执行闪回drop; expect:闪回失败，合理报错
timecapsule table t_timecapsule_0026 to before truncate;

--step7: 查询闪回后的表; expect:查询失败，合理报错
select * from  t_timecapsule_0026 order by a;

--step8: 创建表、插入数据并清空表; expect:表创建成功、数据插入成功且表清空成功
create table t_timecapsule_0026(a int);
insert into t_timecapsule_0026 values(1);
insert into t_timecapsule_0026 values(2);
insert into t_timecapsule_0026 values(3);
truncate table t_timecapsule_0026;

--step9: 在回收站中统计原始对象名称t_timecapsule_0026和操作类型为truncate; expect:预期结果为0
select count(*) from gs_recyclebin where rcyoriginname = 'tab1' and rcyoperation = 't';

--step10: 执行闪回truncate; expect:闪回失败，合理报错
timecapsule table t_timecapsule_0026 to before truncate;

--step11: 查询闪回后的表; expect:查询结果为空与预期结果一致
select * from  t_timecapsule_0026 order by a;

--step12: 清空回收站中的表; expect:清空成功
drop table t_timecapsule_0026 purge;

--step13: 清空回收站; expect:回收站清空成功
purge recyclebin;

--step14: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0026;