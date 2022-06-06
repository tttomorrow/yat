-- @testpoint: 反复执行基于CSN闪回及查询的混合测试

--step1: 查询参数默认值; expect:显示默认值依次为off/0/0
show enable_recyclebin;
show vacuum_defer_cleanup_age;
show version_retention_age;

--step2: 修改参数值; expect:显示结果依次为on/1000/1000
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;
alter system set vacuum_defer_cleanup_age to 1000;
select pg_sleep(2);
show vacuum_defer_cleanup_age;
alter system set version_retention_age to 1000;
select pg_sleep(2);
show version_retention_age;

--step3: 清空回收站; expect:回收站清空成功
purge recyclebin;

--step4: 创建表t_timecapsule_0065_01; expect:表创建成功
drop table if exists t_timecapsule_0065_01;
create table t_timecapsule_0065_01(id int, snaptime timestamptz, snapcsn bigint);

--step5: 创建表t_timecapsule_0065_02后向t_timecapsule_0065_01中插入记录; expect:表创建成功且记录插入成功
create table t_timecapsule_0065_02(a int);
select pg_sleep(4);
insert into t_timecapsule_0065_01 select 1, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step6: 向表t_timecapsule_0065_02插入数据后向t_timecapsule_0065_01中插入记录; expect:插入成功
insert into t_timecapsule_0065_02 values(1),(2),(3);
select pg_sleep(4);
insert into t_timecapsule_0065_01 select 2, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step7: 更新表t_timecapsule_0065_02值后向t_timecapsule_0065_01中插入记录; expect:插入成功
update t_timecapsule_0065_02 set a = 99 where a = 2;
select pg_sleep(4);
insert into t_timecapsule_0065_01 select 3, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step8: 清空表t_timecapsule_0065_02中一条数据后向t_timecapsule_0065_01中插入记录; expect:插入成功
delete from t_timecapsule_0065_02 where a = 3;
select pg_sleep(4);
insert into t_timecapsule_0065_01 select 4, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step9: 向表t_timecapsule_0065_02插入数据后向t_timecapsule_0065_01中插入记录; expect:表创建成功且记录插入成功
insert into t_timecapsule_0065_02 values(4),(5);
select pg_sleep(4);
insert into t_timecapsule_0065_01 select 5, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step10: 查询表t_timecapsule_0065_02数据; expect:查询成功表数据与预期结果一致
select * from t_timecapsule_0065_02 timecapsule timestamp now() order by a;

--step11: 创建函数f_timecapsule_0065_01(); expect:函数创建成功
create or replace function f_timecapsule_0065_01(int8)
  returns integer
  language plpgsql
as
$body$
declare
  count integer;
begin
  count = (select snapcsn from t_timecapsule_0065_01 where id =  $1);
  return count;
end;
$body$;
/
--step12: 创建函数f_timecapsule_0065_02(); expect:函数创建成功
create or replace function f_timecapsule_0065_02(int8)
  returns timestamptz
  language plpgsql
as
$body$
declare
  count timestamptz;
begin
  count = (select snaptime from t_timecapsule_0065_01 where id =  $1);
  return count;
end;
$body$;
/
--step13: 反复执行基于csn闪回查询的混合测试; expect:闪回混合测试成功
timecapsule table t_timecapsule_0065_02 to csn f_timecapsule_0065_01(2);
select * from t_timecapsule_0065_02 timecapsule csn f_timecapsule_0065_01(2) order by a;
timecapsule table t_timecapsule_0065_02 to csn f_timecapsule_0065_01(3);
select * from t_timecapsule_0065_02 timecapsule csn f_timecapsule_0065_01(2) order by a;
timecapsule table t_timecapsule_0065_02 to csn f_timecapsule_0065_01(3);
select * from t_timecapsule_0065_02 timecapsule csn f_timecapsule_0065_01(1) order by a;
timecapsule table t_timecapsule_0065_02 to csn f_timecapsule_0065_01(4);
select * from t_timecapsule_0065_02 timecapsule csn f_timecapsule_0065_01(1) order by a;
timecapsule table t_timecapsule_0065_02 to csn f_timecapsule_0065_01(1);
select * from t_timecapsule_0065_02 timecapsule csn f_timecapsule_0065_01(4) order by a;
timecapsule table t_timecapsule_0065_02 to csn f_timecapsule_0065_01(1);
select * from t_timecapsule_0065_02 timecapsule csn f_timecapsule_0065_01(3) order by a;
timecapsule table t_timecapsule_0065_02 to csn f_timecapsule_0065_01(3);
select * from t_timecapsule_0065_02 timecapsule csn f_timecapsule_0065_01(5) order by a;

--step14: 查询表t_timecapsule_0065_02数据; expect:查询成功数据与预期结果一致
select * from t_timecapsule_0065_02 timecapsule timestamp now() order by a;

--step15: 清理环境 expect:环境清理成功
drop table if exists t_timecapsule_0065_02;
drop table if exists t_timecapsule_0065_01;
drop function if exists f_timecapsule_0065_02();
drop function if exists f_timecapsule_0065_01();
purge recyclebin;

--step16: 恢复默认值; expect:恢复成功，依次显示结果为off/0/0
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;
alter system set vacuum_defer_cleanup_age to 0;
select pg_sleep(2);
show vacuum_defer_cleanup_age;
alter system set version_retention_age to 0;
select pg_sleep(2);
show version_retention_age;