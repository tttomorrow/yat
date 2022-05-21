-- @testpoint: 基表依赖于外部表空间子对象删除,合理报错

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 如果表存在清除表且清除回收站; expect:表清除成功且回收站清除成功
drop table if exists t_timecapsule_0019 ;
purge recyclebin;

--step4: 创建表空间; expect:表空间创建成功
create tablespace ts_timecapsule_0019 relative location 'ts_timecapsule_0019' maxsize '10240k';

--step5: 基于表空间创建表; expect:表创建成功
create table t_timecapsule_0019 (col1 int) tablespace ts_timecapsule_0019;

--step6: 创建索引; expect:索引创建成功
create index i_timecapsule_0019 on t_timecapsule_0019(col1);

--step7: 向表中插入数据; expect:数据插入成功
insert into t_timecapsule_0019 values(1);

--step8: 清空表中的数据; expect:数据清空成功
truncate table t_timecapsule_0019 ;

--step9: 在回收站中截取原始对象名称; expect:截取结果显示两条数据
select substr(rcyoriginname, 1, 9) rcyoriginname, rcyoperation, rcytype, rcycanrestore, rcycanpurge from gs_recyclebin order by rcyrelid;

--step11: 删除表空间; expect:合理报错
drop tablespace ts_timecapsule_0019;

--step12: 删除表并清空回收站; expect:表删除成功且回收站清空成功
drop table t_timecapsule_0019;
purge recyclebin;

--step13: 删除表空间; expect:删除成功
drop tablespace ts_timecapsule_0019;

--step14: 在回收站中截取原始对象名称; expect:截取结果为空
select substr(rcyoriginname, 1, 9) rcyoriginname, rcyoperation, rcytype, rcycanrestore, rcycanpurge from gs_recyclebin order by rcyrelid;

--step15: 清理环境; expect:环境清理成功
drop table if exists t_timecapsule_0019 purge;
purge recyclebin;

--step16: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;