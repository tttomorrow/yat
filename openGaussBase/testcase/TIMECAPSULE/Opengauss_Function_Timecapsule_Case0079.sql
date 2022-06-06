-- @testpoint: 修改表结构后执行csn闪回及闪回查询,合理报错

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

--step4: 创建表t_timecapsule_0079_01; expect:表创建成功
drop table if exists t_timecapsule_0079_01;
create table t_timecapsule_0079_01(id int, snaptime timestamptz, snapcsn bigint);

--step5: 创建表t_timecapsule_0079_02后向t_timecapsule_0079_01中插入记录; expect:表创建成功且记录插入成功
drop table if exists t_timecapsule_0079_02 purge;
create table t_timecapsule_0079_02 (col_1 varchar(255) null default '',col_2 clob default '');
select pg_sleep(4);
insert into t_timecapsule_0079_01 select 1, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step6: 向表t_timecapsule_0079_02插入数据后向t_timecapsule_0079_01中插入记录; expect:插入成功
insert into t_timecapsule_0079_02 values ('ddd',null);
select pg_sleep(4);
insert into t_timecapsule_0079_01 select 2, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step7: 改变表结构后向t_timecapsule_0079_01插入记录; expect:表结构改变成功且记录插入成功
alter table t_timecapsule_0079_02 add col_3 varchar(255) default '';
select pg_sleep(4);
insert into t_timecapsule_0079_01 select 3, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step8: 创建函数f_timecapsule_0079_01(); expect:函数创建成功
create or replace function f_timecapsule_0079_01(int8)
  returns integer
  language plpgsql
as
$body$
declare
  count integer;
begin
  count = (select snapcsn from t_timecapsule_0079_01 where id =  $1);
  return count;
end;
$body$;
/
--step9: 创建函数f_timecapsule_0079_02(); expect:函数创建成功
create or replace function f_timecapsule_0079_02(int8)
  returns timestamptz
  language plpgsql
as
$body$
declare
  count timestamptz;
begin
  count = (select snaptime from t_timecapsule_0079_01 where id =  $1);
  return count;
end;
$body$;
/
--step10: 执行闪回及闪回查询; expect:闪回失败,合理报错
timecapsule table t_timecapsule_0079_02 to csn f_timecapsule_0079_01(1);
select * from t_timecapsule_0079_02 timecapsule csn f_timecapsule_0079_01(1) order by COL_1;
timecapsule table t_timecapsule_0079_02 to csn f_timecapsule_0079_01(2);
select * from t_timecapsule_0079_02 timecapsule csn f_timecapsule_0079_01(2) order by COL_1;


--step11: 执行闪回及闪回查询修改表结构前; expect:闪回及闪回成功
timecapsule table t_timecapsule_0079_02 to csn f_timecapsule_0079_01(3);
select * from t_timecapsule_0079_02 timecapsule csn f_timecapsule_0079_01(3) order by COL_1;

--step12: 清理环境 expect:环境清理成功
drop table if exists t_timecapsule_0079_02;
drop table if exists t_timecapsule_0079_01;
drop function if exists f_timecapsule_0079_02();
drop function if exists f_timecapsule_0079_01();
purge recyclebin;

--step13: 恢复默认值; expect:恢复成功，依次显示结果为off/0/0
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;
alter system set vacuum_defer_cleanup_age to 0;
select pg_sleep(2);
show vacuum_defer_cleanup_age;
alter system set version_retention_age to 0;
select pg_sleep(2);
show version_retention_age;