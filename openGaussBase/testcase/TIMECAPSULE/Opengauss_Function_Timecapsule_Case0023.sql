-- @testpoint: 子对象删除,子对象索引依赖外部函数

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 如果表存在清除表且清除回收站; expect:表清除成功且回收站清除成功
drop table if exists t_timecapsule_0023;
purge recyclebin;

--step4: 创建函数; expect:函数创建成功
create function f_timecapsule_0023(int) returns int
as $$ select $1::int $$ language sql;
/
--step5: 创建表; expect:表创建成功
create table t_timecapsule_0023 (a int, b int);

--step6: 创建索引; expect:索引创建成功
create index i_timecapsule_0023_01 on t_timecapsule_0023 (f_timecapsule_0023(b));
create index i_timecapsule_0023_02 on t_timecapsule_0023 (a);

--step7: 在回收站中截取原始对象名称; expect:截取显示结果为空
select substr(rcyoriginname, 1, 9) rcyoriginname, rcyoperation, rcytype, rcycanrestore, rcycanpurge from gs_recyclebin order by rcyrelid;

--step8: 删除表; expect:删除成功
drop table t_timecapsule_0023;

--step9: 在回收站中截取原始对象名称; expect:截取结果显示两条数据
select substr(rcyoriginname, 1, 9) rcyoriginname, rcyoperation, rcytype, rcycanrestore, rcycanpurge from gs_recyclebin order by rcyrelid;

--step10: 清空回收站; expect:回收站清空成功
purge recyclebin;

--step11: 删除函数; expect:函数删除成功
drop function f_timecapsule_0023(int);

--step12: 在回收站中截取原始对象名称; expect:截取结果为空
select substr(rcyoriginname, 1, 9) rcyoriginname, rcyoperation, rcytype, rcycanrestore, rcycanpurge from gs_recyclebin order by rcyrelid;

--step13: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0023 purge;

--step14: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;