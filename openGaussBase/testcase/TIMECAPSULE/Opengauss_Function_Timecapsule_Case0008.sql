-- @testpoint: 执行闪回drop,从回收站中检索的表指定一个新名称,合理报错

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清除回收站; expect:回收站清除成功
purge recyclebin;

--step4: 创建表; expect:表创建成功
drop table if exists t_timecapsule_0008_01;
create table t_timecapsule_0008_01(a int);

--step5: 创建唯一索引; expect:索引创建成功
create unique index i_timecapsule_0008 on t_timecapsule_0008_01(a);

--step6: 向表中插入数据; expect:数据插入成功
insert into t_timecapsule_0008_01 values(1);
insert into t_timecapsule_0008_01 values(2);
insert into t_timecapsule_0008_01 values(3);

--step7: 向表中插入已有数据; expect:数据插入失败
insert into t_timecapsule_0008_01 values(1);

--step8: 删除drop表; expect:删除成功
drop table t_timecapsule_0008_01;

--step9: 统计索引数量; expect:预期结果为0
select count(*) from pg_indexes where indexname = 'i_timecapsule_0008';

--step10: 向表中插入已有数据; expect:数据插入失败
insert into t_timecapsule_0008_01 values(1);

--step11: 在回收站中统计原始对象名称%_timecapsule_0008%和操作类型为drop; expect:预期结果为2
select count(*) from gs_recyclebin where rcyoriginname like '%_timecapsule_0008%' and rcyoperation = 'd';

--step12: 从回收站中检索的表指定一个新名称t_timecapsule_0008_01; expect:新名称指定成功
timecapsule table t_timecapsule_0008_01 to before drop rename to t_timecapsule_0008_02;

--step13: 查询表新名称t_timecapsule_0008_02; expect:预期结果为1
select count(*) from pg_indexes where tablename = 't_timecapsule_0008_02';

--step14: 在回收站中统计原始对象名称%_timecapsule_0008%和操作类型为drop; expect:预期结果为0
select count(*) from gs_recyclebin where rcyoriginname like '%_timecapsule_0008%' and rcyoperation = 'd';

--step15: 查询旧表t_timecapsule_0008_01; expect:查询失败
select * from t_timecapsule_0008_01 order by a;

--step16: 查询闪回后新表t_timecapsule_0008_02; expect:显示结果为3条数据
select * from t_timecapsule_0008_02 order by a;

--step17: 向闪回后的新表中插入已有数据; expect:数据插入失败
insert into t_timecapsule_0008_02 values(1);

--step18: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0008_01 purge;
drop table if exists t_timecapsule_0008_02 purge;
purge recyclebin;

--step19: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;