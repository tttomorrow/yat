-- @testpoint: 闪回drop并发，开启两个事务,一个做闪回drop,另一个做purge table时合理报错

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 如果表存在清除表且清除回收站; expect:表清除成功且回收站清除成功
drop table if exists t_timecapsule_0061;
purge recyclebin;

--step4: 创建表、插入数据且删除表数据; expect:表创建成功、数据插入成功且表删除成功
create table t_timecapsule_0061(a int, b int);
insert into t_timecapsule_0061 values (1,1);
drop table t_timecapsule_0061;

--step5: 开启事务做闪回; expect:闪回成功
start transaction;
timecapsule table t_timecapsule_0061 to before drop;
commit;

--step6: 清空回收站中指定的表; expect:清空回收站中指定表成功失败合理报错
start transaction;
purge table t_timecapsule_0061;
commit;

--step7: 查询闪回后的表; expect:查询结果为1条数据与预期结果一致
select * from t_timecapsule_0061;

--step8: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0061 purge;
purge recyclebin;

--step9: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;
