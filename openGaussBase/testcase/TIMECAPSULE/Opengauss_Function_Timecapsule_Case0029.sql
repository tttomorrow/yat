-- @testpoint: 不支持闪回drop,truncate全局临时表,合理报错

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 如果表存在清除表且清除回收站; expect:表清除成功且回收站清除成功
drop table if exists t_timecapsule_0029 ;
purge recyclebin;

--step4: 创建全局临时表; expect:表创建成功
create global temporary table t_timecapsule_0029
(
    id                        integer               not null,
    name                      char(16)              not null,
    address                   varchar(50)                   ,
    postcode                  char(6)
);

--step5:向表中插入数据; expect:数据插入成功
insert into t_timecapsule_0029 values(1, 'tom', 'jiexiu', '032000');

--step6: 清空表; expect:表清空成功
truncate table t_timecapsule_0029;

--step7: 执行闪回truncate; expect:闪回失败合理报错
timecapsule table t_timecapsule_0029 to before truncate;

--step8: 删除表; expect:表删除成功
drop table t_timecapsule_0029;

--step9: 执行闪回drop; expect:闪回失败合理报错
timecapsule table t_timecapsule_0029 to before drop;

--step10: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0029 purge;
purge recyclebin;

--step11: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;