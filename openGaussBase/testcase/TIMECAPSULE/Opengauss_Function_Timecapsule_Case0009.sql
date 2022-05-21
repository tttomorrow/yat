-- @testpoint: 执行闪回truncate,合理报错

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清除回收站; expect:回收站清除成功
purge recyclebin;

--step4: 创建表; expect:表创建成功
drop table if exists t_timecapsule_0009;
create table t_timecapsule_0009(a int);

--step5: 创建唯一索引; expect:索引创建成功
create unique index i_timecapsule_0009 on t_timecapsule_0009(a);

--step6: 向表中插入数据; expect:数据插入成功
insert into t_timecapsule_0009 values(1);
insert into t_timecapsule_0009 values(2);
insert into t_timecapsule_0009 values(3);

--step7: 向表中插入已有数据; expect:数据插入失败
insert into t_timecapsule_0009 values(1);

--step7: 清空表数据; expect:表数据清空成功
truncate table t_timecapsule_0009;

--step8: 向表中插入数据; expect:数据插入成功
insert into t_timecapsule_0009 values(1);

--step9: 在回收站中统计原始对象名称%_timecapsule_0009%和操作类型为truncate; expect:预期结果为2
select count(*) from gs_recyclebin where rcyoriginname like '%_timecapsule_0009%' and rcyoperation = 't';

--step10: 闪回语句语法错误闪回到truncate之前; expect:闪回失败
timecapsule idx i_timecapsule_0009 to before truncate;

--step11: 闪回语句表名错误闪回到truncate之前; expect:闪回失败
timecapsule table i_timecapsule_0009 to before truncate;

--step12: 闪回到truncate之前; expect:闪回成功
timecapsule table t_timecapsule_0009 to before truncate;

--step13: 在回收站中统计原始对象名称%_timecapsule_0009%和操作类型为truncate; expect:预期结果为2
select count(*) from gs_recyclebin where rcyoriginname like '%_timecapsule_0009%' and rcyoperation = 't';

--step14: 查询闪回后的表数据; expect:显示3条数据
select * from t_timecapsule_0009 order by a;

--step15: 向闪回后的表中插入已有的数据; expect:插入数据失败
insert into t_timecapsule_0009 values(1);

--step16: 删除索引; expect:索引删除成功
drop index i_timecapsule_0009;

--step17: 在回收站中统计原始对象名称%_timecapsule_0009%和操作类型为truncate; expect:预期结果为2
select count(*) from gs_recyclebin where rcyoriginname like '%_timecapsule_0009%' and rcyoperation = 't';

--step18: 清理环境; expect:清理成功
drop table t_timecapsule_0009 purge;
purge recyclebin;

--step19: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;