-- @testpoint: 子对象删除,触发器依赖外部PLPGSQL函数

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 如果表存在清除表且清除回收站; expect:表清除成功且回收站清除成功
drop table if exists t_timecapsule_0025;
purge recyclebin;

--step4: 创建函数; expect:函数创建成功
create or replace function f_timecapsule_0025() returns trigger as
$$
declare
begin
       return new;
end
$$ language plpgsql;
/
--step5: 创建表; expect:表创建成功
create table t_timecapsule_0025(c1 int, c2 int);

--step6: 创建触发器; expect:触发器创建成功
create trigger trig_timecapsule_0025
before insert on t_timecapsule_0025
for each row
execute procedure f_timecapsule_0025();
/
--step7: 查询触发器; expect:查询结果为新建的触发器名称
select tgname  from pg_trigger where tgname = 'trig_timecapsule_0025';

--step8: 删除表; expect:删除成功
drop table t_timecapsule_0025;

--step9: 查询触发器; expect:查询结果为空
select tgname  from pg_trigger where tgname = 'trig_timecapsule_0025';

--step10: 删除函数; expect:
drop function f_timecapsule_0025();

--step11: 清空回收站; expect:回收站清空成功
purge recyclebin;

--step12: 在回收站中截取原始对象名称; expect:截取显示结果为空
select substr(rcyoriginname, 1, 9) rcyoriginname, rcyoperation, rcytype, rcycanrestore, rcycanpurge from gs_recyclebin order by rcyrelid;

--step13: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0025;

--step14: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;