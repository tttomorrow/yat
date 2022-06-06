-- @testpoint: 验证enable_recyclebin 边界值异常值为1,0,值为0时合理报错

--step1: 查询enable_recyclebin 默认值; expect:显示默认值
show enable_recyclebin;

--step2: 修改enable_recyclebin为1; expect:显示值为on
alter system set enable_recyclebin to 1;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清空回收站; expect:回收站清空成功
drop table if exists t_timecapsule_0035 purge;
purge recyclebin;

--step4: 创建表、插入数据且清空表数据; expect:表创建成功、数据插入成功且清空表数据成功
create table t_timecapsule_0035(a int);
insert into t_timecapsule_0035 values(1);
insert into t_timecapsule_0035 values(2);
insert into t_timecapsule_0035 values(3);
truncate table t_timecapsule_0035;

--step5: 执行truncate闪回; expect:闪回成功
timecapsule table t_timecapsule_0035 to before truncate;

--step6: 查询闪回的表数据; expect:查询结果为3条数据与预期结果一致
select * from  t_timecapsule_0035;

--step7: 删除表; expect:表删除成功
drop table t_timecapsule_0035;

--step8: 执行drop闪回; expect:闪回成功
timecapsule table t_timecapsule_0035 to before drop;

--step9: 查询闪回的表数据; expect:查询结果为3条数据与预期结果一致
select * from  t_timecapsule_0035;

--step10: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0035 purge;
purge recyclebin;

--step11: 查询enable_recyclebin值; expect:预期结果为on
show enable_recyclebin;

--step12: 修改enable_recyclebin为0; expect:显示值为off
alter system set enable_recyclebin to 0;
select pg_sleep(2);
show enable_recyclebin;

--step13: 创建表、插入数据且清空表数据; expect:表创建成功、数据插入成功且清空表数据成功
drop table if exists t_timecapsule_0035;
create table t_timecapsule_0035(a int);
insert into t_timecapsule_0035 values(1);
insert into t_timecapsule_0035 values(2);
insert into t_timecapsule_0035 values(3);
truncate table t_timecapsule_0035;

--step14: 执行truncate闪回; expect:闪回失败，合理报错
timecapsule table t_timecapsule_0035 to before truncate;

--step15: 删除表; expect:表删除成功
drop table t_timecapsule_0035;

--step16: 执行drop闪回; expect:闪回失败，合理报错
timecapsule table t_timecapsule_0035 to before drop;

--step17: 清理环境; expect:环境清理成功
drop table if exists t_timecapsule_0035 purge;
purge recyclebin;

--step18: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;