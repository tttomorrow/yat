-- @testpoint: rollback事务后执行csn闪回查询,合理报错

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

--step4: 创建表t_timecapsule_0083_01; expect:表创建成功
drop table if exists t_timecapsule_0083_01;
create table t_timecapsule_0083_01(id int, snaptime timestamptz, snapcsn bigint);

--step5: 创建表t_timecapsule_0083_02后向t_timecapsule_0083_01中插入记录; expect:表创建成功且记录插入成功
create table t_timecapsule_0083_02
(
  r_reason_sk    integer,
  r_reason_id    character(16),
  r_reason_desc  character(100)
);
select pg_sleep(4);
insert into t_timecapsule_0083_01 select 1, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step6: 开启事务; expect:事务开启成功
start transaction;

--step7: 向表t_timecapsule_0083_02插入数据后向t_timecapsule_0083_01中插入记录; expect:插入成功
insert into t_timecapsule_0083_02(r_reason_sk, r_reason_id, r_reason_desc) values (1, 'aaaaaaaaaaaaaaaa', 'reason1');
select pg_sleep(4);
insert into t_timecapsule_0083_01 select 2, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();
insert into t_timecapsule_0083_02(r_reason_sk, r_reason_id, r_reason_desc) values (2, 'abbbbbbbbbbbbbba', 'reason2');
select pg_sleep(4);
insert into t_timecapsule_0083_01 select 3, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step8: 回滚事务; expect:事务回滚成功
rollback;

--step9: 向表t_timecapsule_0083_02插入数据后向t_timecapsule_0083_01中插入记录; expect:插入成功
insert into t_timecapsule_0083_02(r_reason_sk, r_reason_id, r_reason_desc) values (3, 'acccccccccccccca', 'reason3');
select pg_sleep(4);
insert into t_timecapsule_0083_01 select 4, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step10: 创建函数f_timecapsule_0083_01(); expect:函数创建成功
create or replace function f_timecapsule_0083_01(int8)
  returns integer
  language plpgsql
as
$body$
declare
  count integer;
begin
  count = (select snapcsn from t_timecapsule_0083_01 where id =  $1);
  return count;
end;
$body$;
/
--step11: 创建函数f_timecapsule_0083_02(); expect:函数创建成功
create or replace function f_timecapsule_0083_02(int8)
  returns timestamptz
  language plpgsql
as
$body$
declare
  count timestamptz;
begin
  count = (select snaptime from t_timecapsule_0083_01 where id =  $1);
  return count;
end;
$body$;
/
--step12: 执行闪回及闪回查询开启事务之前; expect:闪回成功
timecapsule table t_timecapsule_0083_02 to csn f_timecapsule_0083_01(1);
select * from t_timecapsule_0083_02 timecapsule csn f_timecapsule_0083_01(1) order by r_reason_sk;

--step13: 在回滚前执行闪回及闪回查询; expect:合理报错
timecapsule table t_timecapsule_0083_02 to csn f_timecapsule_0083_01(2);
select * from t_timecapsule_0083_02 timecapsule csn f_timecapsule_0083_01(2) order by r_reason_sk;
timecapsule table t_timecapsule_0083_02 to csn f_timecapsule_0083_01(3);
select * from t_timecapsule_0083_02 timecapsule csn f_timecapsule_0083_01(3) order by r_reason_sk;

--step14 回滚后执行闪回及闪回查询; expect:闪回成功
timecapsule table t_timecapsule_0083_02 to csn f_timecapsule_0083_01(4);
select * from t_timecapsule_0083_02 timecapsule csn f_timecapsule_0083_01(4) order by r_reason_sk;

--step15: 清理环境 expect:环境清理成功
drop table if exists t_timecapsule_0083_02;
drop table if exists t_timecapsule_0083_01;
drop function if exists f_timecapsule_0083_02();
drop function if exists f_timecapsule_0083_01();
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