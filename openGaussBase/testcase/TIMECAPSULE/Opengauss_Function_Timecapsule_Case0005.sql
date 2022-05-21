-- @testpoint: 清空回收站中指定的索引,部分测试点合理报错


--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清除回收站; expect:回收站清除成功
purge recyclebin;

--step4: 创建表、插入数据; expect:表创建成功、数据插入成功
drop table if exists t_timecapsule_0005;
create table t_timecapsule_0005(a int);
insert into t_timecapsule_0005 values(1);
insert into t_timecapsule_0005 values(2);
insert into t_timecapsule_0005 values(3);

--step5: 创建唯一索引; expect:索引创建成功
create unique index  i_timecapsule_0005 on t_timecapsule_0005(a);

--step6: 向表插入已有的值; expect:数据插入失败
insert into t_timecapsule_0005 values(3);

--step7: 删除表; expect:删除成功
drop table t_timecapsule_0005;

--step8: 在回收站中统计原始对象名称t_timecapsule_0005%和操作类型为drop; expect:预期结果为2
select count(*) from gs_recyclebin where rcyoriginname like '%_timecapsule_0005%' and rcyoperation = 'd';

--step9: 清除回收站中指定索引; expect:索引清除成功
purge index i_timecapsule_0005;

--step10: 在回收站中统计原始对象名称t_timecapsule_0005和操作类型为drop; expect:预期结果为1
select count(*) from gs_recyclebin where rcyoriginname like '%_timecapsule_0005%' and rcyoperation = 'd';

--step11: 执行闪回drop; expect:闪回成功
timecapsule table t_timecapsule_0005 to before drop;

--step12: 向表插入已有的值; expect:数据插入成功
insert into t_timecapsule_0005 values(3);

--step13: 查询闪回后的表; expect:成功显示四条数据
select * from t_timecapsule_0005 order by a;

--step14: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0005 purge;
purge recyclebin;

--step15: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;