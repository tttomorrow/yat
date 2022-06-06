-- @testpoint: 不支持闪回TRUNCATE TABLE命令同时指定多个对象,合理报错

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清除回收站; expect:回收站清除成功
drop table if exists t_timecapsule_0028_01 ;
drop table if exists t_timecapsule_0028_02 ;
purge recyclebin;

--step4: 创建表两个表且插入数据; expect:表创建成功且数据插入成功
create table t_timecapsule_0028_01(a int);
insert into t_timecapsule_0028_01 values(1);
insert into t_timecapsule_0028_01 values(2);
insert into t_timecapsule_0028_01 values(3);
create table t_timecapsule_0028_02(a int);
insert into t_timecapsule_0028_02 values(1);
insert into t_timecapsule_0028_02 values(2);
insert into t_timecapsule_0028_02 values(3);

--step5: 清空两个表; expect:表清空成功
truncate table t_timecapsule_0028_01,t_timecapsule_0028_02;

--step6: 对表1执行truncate闪回; expect:闪回失败合理报错
timecapsule table t_timecapsule_0028_01 to before truncate;

--step7: 对表2执行truncate闪回; expect:闪回失败合理报错
timecapsule table t_timecapsule_0028_02 to before truncate;

--step8: 对两个表同时执行truncate闪回; expect:闪回失败合理报错
timecapsule table t_timecapsule_0028_01,t_timecapsule_0028_02 to before truncate;

--step9: 删除表; expect:表删除成功
drop table t_timecapsule_0028_01,t_timecapsule_0028_02;

--step10: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0028_01 purge;
drop table if exists t_timecapsule_0028_02 purge;

--step11: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;