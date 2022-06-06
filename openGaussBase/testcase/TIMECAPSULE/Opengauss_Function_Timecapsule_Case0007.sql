-- @testpoint: 执行drop闪回,合理报错

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清除回收站; expect:回收站清除成功
purge recyclebin;

--step4: 创建表、插入数据; expect:表创建成功、数据插入成功
drop table if exists t_timecapsule_0007;
create table t_timecapsule_0007(a int);
insert into t_timecapsule_0007 values(1);

--step5: 创建唯一索引; expect:索引创建成功
create unique index i_timecapsule_0007 on t_timecapsule_0007(a);

--step6: 删除drop表; expect:删除成功
drop table t_timecapsule_0007;

--step7: 在回收站中统计原始对象名称%_timecapsule_0007%和操作类型为drop; expect:预期结果为2
select count(*) from gs_recyclebin where rcyoriginname like '%_timecapsule_0007%' and rcyoperation = 'd';

--step8: 执行闪回drop语法错误; expect:闪回失败
timecapsule idx i_timecapsule_0007 to before drop;

--step9: 执行闪回drop表名错误; expect:闪回失败
timecapsule table i_timecapsule_0007 to before drop;

--step10: 执行闪回drop; expect:闪回成功
timecapsule table t_timecapsule_0007 to before drop;

--step11: 查询闪回后的表; expect:成功显示数据1
select * from t_timecapsule_0007;

--step12: 向闪回后的表中插入已有的数据; expect:插入失败
insert into t_timecapsule_0007 values(1);

--step13: 在回收站中统计原始对象名称%_timecapsule_0007%和操作类型为drop; expect:预期结果为0
select count(*) from gs_recyclebin where rcyoriginname like '%_timecapsule_0007%' and rcyoperation = 'd';

--step14: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0007 purge;
purge recyclebin;

--step14: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;