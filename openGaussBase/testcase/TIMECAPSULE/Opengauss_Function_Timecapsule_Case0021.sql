-- @testpoint: 支持检查约束依赖于外部对象函数的闪回

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清空回收站; expect:回收站清空成功
drop table if exists t_timecapsule_0021;
purge recyclebin;

--step4: 创建函数; expect:函数创建成功
create function f_timecapsule_0021() returns int
as $$ select 1::int $$ language sql;
/
--step5: 创建表; expect:表创建成功
create table t_timecapsule_0021 (c1 int check (c1 + f_timecapsule_0021() > 0), c2 int check(c2 > c1));

--step6: 从系统表中检查约束; expect:会显示两条数据
select contype, conkey, conexclop, consrc from pg_constraint where oid > 16383 and consrc like '%c1%';

--step7: 删除表; expect:表删除成功
drop table t_timecapsule_0021;

--step8: 从系统表中检查约束; expect:显示一条数据
select contype, conkey, conexclop, consrc from pg_constraint where oid > 16383 and consrc like '%c1%';

--step9: 在回收站中截取原始对象名称; expect:显示一条回收站中表的数据
select substr(rcyoriginname, 1, 9) rcyoriginname, rcyoperation, rcytype, rcycanrestore, rcycanpurge from gs_recyclebin order by rcyrelid;

--step10: 在回收站中统计原始对象名称t_timecapsule_0021和操作类型为drop; expect:预期结果为1
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0021' and rcyoperation = 'd';

--step11: 执行闪回drop; expect:闪回成功
timecapsule table t_timecapsule_0021 to before drop;

--step12: 查询闪回后的表; expect:查询结果为空与预期结果一致
select * from t_timecapsule_0021;

--step13: 从系统表中检查约束; expect:显示一条数据
select contype, conkey, conexclop, consrc from pg_constraint where oid > 16383 and consrc like '%c1%';

--step14: 删除函数、表并清空回收站; expect:函数、表删除成功且回收站清空成功
drop function if exists f_timecapsule_0021();
drop table if exists t_timecapsule_0021 purge;
purge recyclebin;

--step15: 在回收站中截取原始对象名称; expect:截取结果为空
select substr(rcyoriginname, 1, 9) rcyoriginname, rcyoperation, rcytype, rcycanrestore, rcycanpurge from gs_recyclebin order by rcyrelid;

--step16: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0021 purge;

--step17: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;