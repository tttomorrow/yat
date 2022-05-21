-- @testpoint: 在事务中闪回

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

--step4: 创建函数f_timecapsule_0095(); expect:函数创建成功
create or replace function f_timecapsule_0095(int8)
  returns integer
  language plpgsql
as
$body$
declare
  count integer;
begin
  count = (select snapcsn from t_timecapsule_0095_01 where id =  $1);
  return count;
end;
$body$;
/
--step5: 创建表; expect:表创建成功
drop table if exists t_timecapsule_0095_01;
create table t_timecapsule_0095_01(id int, snaptime timestamptz, snapcsn bigint);

--step6: 创建表并向t_timecapsule_0095_01表中插入数据; expect:表创建成功且数据插入成功
drop table if exists t_timecapsule_0095_02;
create table t_timecapsule_0095_02
(
  r_reason_sk    integer,
  r_reason_id    character(16),
  r_reason_desc  character(100)
);
select pg_sleep(4);
insert into t_timecapsule_0095_01 select 1, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step7: 开启事务; expect:事务开启成功
start transaction;

--step8: 在事务中向表中插入数据; expect:数据插入成功
insert into t_timecapsule_0095_02(r_reason_sk, r_reason_id, r_reason_desc) values (1, 'aaaaaaaaaaaaaaaa', 'reason1');
select pg_sleep(4);
insert into t_timecapsule_0095_01 select 2, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step9: 在事务中查询表2; expect:查询结果为插入数据
select * from t_timecapsule_0095_02;
select * from t_timecapsule_0095_01;


--step10: 在事务中向表中插入数据; expect:数据插入成功
insert into t_timecapsule_0095_02(r_reason_sk, r_reason_id, r_reason_desc) values (2, 'abbbbbbbbbbbbbba', 'reason2');
select pg_sleep(4);
insert into t_timecapsule_0095_01 select 3, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step11: 在事务中执行csn闪回及闪回查询; expect:闪回成功但闪回查询无数据显示
timecapsule table t_timecapsule_0095_02 to csn f_timecapsule_0095(1);
select * from t_timecapsule_0095_02 timecapsule csn f_timecapsule_0095(1) order by r_reason_sk;

timecapsule table t_timecapsule_0095_02 to csn f_timecapsule_0095(2);
select * from t_timecapsule_0095_02 timecapsule csn f_timecapsule_0095(2) order by r_reason_sk;

timecapsule table t_timecapsule_0095_02 to csn f_timecapsule_0095(3);
select * from t_timecapsule_0095_02 timecapsule csn f_timecapsule_0095(3) order by r_reason_sk;

--step12: 在事务中再次插入表数据; expect:数据插入成功
select pg_sleep(4);
insert into t_timecapsule_0095_01 select 4, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step13: 提交事务; expect:事务提交成功
commit;

--step14: 提交事务后插入数据; expect:数据插入成功
insert into t_timecapsule_0095_02(r_reason_sk, r_reason_id, r_reason_desc) values (3, 'acccccccccccccca', 'reason3');
select pg_sleep(4);
insert into t_timecapsule_0095_01 select 5, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step15: 提交事务执行闪回及闪回查询; expect:闪回及闪回查询成功
timecapsule table t_timecapsule_0095_02 to csn f_timecapsule_0095(4);
select * from t_timecapsule_0095_02 timecapsule csn f_timecapsule_0095(4) order by r_reason_sk;
timecapsule table t_timecapsule_0095_02 to csn f_timecapsule_0095(5);
select * from t_timecapsule_0095_02 timecapsule csn f_timecapsule_0095(5) order by r_reason_sk;

--step16: 查询闪回后的表; expect:查询结果与预期结果一致
select * from t_timecapsule_0095_02;

--step17: 清理环境 expect:环境清理成功
drop table if exists t_timecapsule_0095_02 purge;
drop table if exists t_timecapsule_0095_01 cascade;
drop function if exists  f_timecapsule_0095();
purge recyclebin;

--step18: 恢复默认值; expect:恢复成功，依次显示结果为off/0/0
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;
alter system set vacuum_defer_cleanup_age to 0;
select pg_sleep(2);
show vacuum_defer_cleanup_age;
alter system set version_retention_age to 0;
select pg_sleep(2);
show version_retention_age;