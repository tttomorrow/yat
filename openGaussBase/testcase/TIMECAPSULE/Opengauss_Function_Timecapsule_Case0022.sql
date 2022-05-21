-- @testpoint: 子对象删除，子对象视图1依赖外部对象表2

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清除回收站; expect:回收站清除成功
purge recyclebin;

--step4: 创建模式; expect:模式创建成功
drop schema if exists s_timecapsule_0022;
create schema s_timecapsule_0022;

--step5: 创建表; expect:表创建成功
drop table if exists s_timecapsule_0022.t_timecapsule_0022_01;
drop table if exists s_timecapsule_0022.t_timecapsule_0022_02;
create table s_timecapsule_0022.t_timecapsule_0022_01(c1 int);
create table s_timecapsule_0022.t_timecapsule_0022_02(c1 int);

--step6: 向表中插入数据; expect:数据插入成功
insert into s_timecapsule_0022.t_timecapsule_0022_01 values(1);
insert into s_timecapsule_0022.t_timecapsule_0022_02 values(1);

--step7: 创建视图; expect:视图创建成功
create view s_timecapsule_0022.v_timecapsule_0022_01 as select 'v_timecapsule_0022_01' from s_timecapsule_0022.t_timecapsule_0022_01, s_timecapsule_0022.t_timecapsule_0022_02;
create view s_timecapsule_0022.v_timecapsule_0022_02 as select 'v_timecapsule_0022_02' from s_timecapsule_0022.t_timecapsule_0022_02;

--step8: 查询模式; expect:查询成功显示2条数据
select schemaname, substr(viewname, 1, 4) viewname, substr(definition, 1, 17) definition from pg_views where schemaname = 's_timecapsule_0022';

--step9: 查询规则名称; expect:查询成功显示2条数据
select rulename, substr(ev_class::regclass::text, 1, 5) ev_class from pg_rewrite where oid >16383 and ev_class::regclass::text like '%s_timecapsule_0022.v_timecapsule_0022%' order by oid;

--step10: 删除表; expect:表删除成功
drop table s_timecapsule_0022.t_timecapsule_0022_01 cascade;
drop table s_timecapsule_0022.t_timecapsule_0022_02 cascade;

--step11: 在回收站中清除表1; expect:表清除成功
purge table s_timecapsule_0022.t_timecapsule_0022_01;

--step12: 查询模式; expect:查询成功显示1条数据
select schemaname, substr(viewname, 1, 4) viewname, substr(definition, 1, 17) definition from pg_views where schemaname = 's_timecapsule_0022';

--step12: 查询规则名称; expect:查询成功显示1条数据
select rulename, substr(ev_class::regclass::text, 1, 5) ev_class from pg_rewrite where oid >16383 and ev_class::regclass::text like 's_timecapsule_0022.%' order by oid;

--step13:对表2执行闪回; expect:闪回成功
timecapsule table s_timecapsule_0022.t_timecapsule_0022_02 to before drop;

--step14:对表2进行查询; expect:查询结果为1与预期结果一致
select* from  s_timecapsule_0022.t_timecapsule_0022_02;

--step15:匿名块执行; expect:执行成功
declare
    vname TEXT;
    tmp TEXT;
begin
    select viewname into vname from pg_views where viewname like '%BIN$%';
    execute immediate 'select * from s_timecapsule_0022."' || vname || '"' into tmp;
    raise warning 'query v_timecapsule_0022_02: %', tmp;
end;
/

--step16:删除表2; expect:删除成功
drop table s_timecapsule_0022.t_timecapsule_0022_02 cascade;

--step17:对表2执行闪回; expect:闪回成功
timecapsule table s_timecapsule_0022.t_timecapsule_0022_02 to before drop;

--step18:对表2进行查询; expect:查询结果为1与预期结果一致
select* from  s_timecapsule_0022.t_timecapsule_0022_02;

--step19:匿名块执行; expect:执行成功
declare
    vname TEXT;
    tmp TEXT;
begin
    select viewname into vname from pg_views where viewname like '%BIN$%';
    execute immediate 'select * from s_timecapsule_0022."' || vname || '"' into tmp;
    raise warning 'query v_timecapsule_0022_02: %', tmp;
end;
/

--step20:删除表; expect:表删除成功
drop table s_timecapsule_0022.t_timecapsule_0022_02 cascade purge;

--step21:删除模式; expect:表删除成功
purge recyclebin;
drop schema s_timecapsule_0022;

--step22: 在回收站中截取原始对象名称; expect:显示结果为0条数据
select substr(rcyoriginname, 1, 9) rcyoriginname, rcyoperation, rcytype, rcycanrestore, rcycanpurge from gs_recyclebin order by rcyrelid;
select substr(rcyoriginname, 1, 9) rcyoriginname, rcyoperation, rcytype, rcycanrestore, rcycanpurge from gs_recyclebin order by rcyrelid;

--step23: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;