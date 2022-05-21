-- @testpoint: 不支持闪回DROP TABLE命令同时指定多个对象,合理报错

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清除回收站; expect:回收站清除成功
drop table if exists t_t_timecapsule_0027_01;
drop table if exists t_t_timecapsule_0027_02;
purge recyclebin;

--step4: 创建表两个表且插入数据; expect:表创建成功且数据插入成功
create table t_t_timecapsule_0027_01(a int);
insert into t_t_timecapsule_0027_01 values(1);
insert into t_t_timecapsule_0027_01 values(2);
insert into t_t_timecapsule_0027_01 values(3);
create table t_t_timecapsule_0027_02(a int);
insert into t_t_timecapsule_0027_02 values(1);
insert into t_t_timecapsule_0027_02 values(2);
insert into t_t_timecapsule_0027_02 values(3);

--step5: 删除两个表; expect:表删除成功
drop table t_t_timecapsule_0027_01,t_t_timecapsule_0027_02;

--step6: 对表1执行drop闪回; expect:闪回失败合理报错
timecapsule table t_t_timecapsule_0027_01 to before drop;

--step7: 对表2执行drop闪回; expect:闪回失败合理报错
timecapsule table t_t_timecapsule_0027_02 to before drop;

--step8: 对两个表同时执行drop闪回; expect:闪回失败合理报错
timecapsule table t_t_timecapsule_0027_01,t_t_timecapsule_0027_02 to before drop;

--step9: 清理环境; expect:清理成功
drop table if exists t_t_timecapsule_0027_01 purge;
drop table if exists t_t_timecapsule_0027_02 purge;
purge recyclebin;

--step10: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;