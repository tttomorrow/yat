-- @testpoint: truncate后物理删除不可闪回,合理报错

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清除回收站; expect:回收站清除成功
purge recyclebin;

--step4: 创建表; expect:表创建成功
drop table if exists  t_timecapsule_0010;
create table t_timecapsule_0010(a int);

--step5: 向表中插入数据; expect:数据插入成功
insert into t_timecapsule_0010 values(1);

--step6: 清空表数据; expect:表数据清空成功
truncate table t_timecapsule_0010;

--step7: 在回收站中统计原始对象名称t_timecapsule_0010和操作类型为truncate; expect:预期结果为1
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0010' and rcyoperation = 't';

--step8: 清除表; expect:清除成功
drop table t_timecapsule_0010 purge;

--step9: 闪回到truncate之前; expect:闪回失败
timecapsule table t_timecapsule_0010 to before truncate;

--step10: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0010 purge;
purge recyclebin;

--step11: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;