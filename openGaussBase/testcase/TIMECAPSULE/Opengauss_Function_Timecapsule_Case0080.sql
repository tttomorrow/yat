-- @testpoint: vacuum full表后执行csn闪回及闪回查询,合理报错

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

--step4: 创建表t_timecapsule_0080_01; expect:表创建成功
drop table if exists t_timecapsule_0080_01;
create table t_timecapsule_0080_01(id int, snaptime timestamptz, snapcsn bigint);

--step5: 创建表t_timecapsule_0080_02后向t_timecapsule_0080_01中插入记录; expect:表创建成功且记录插入成功
create table t_timecapsule_0080_02
(
   stuno     int,
   classno   int
);
select pg_sleep(4);
insert into t_timecapsule_0080_01 select 1, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step6: 向表t_timecapsule_0080_02插入数据后向t_timecapsule_0080_01中插入记录; expect:插入成功
insert into t_timecapsule_0080_02 values(1,1);
insert into t_timecapsule_0080_02 values(2,2);
insert into t_timecapsule_0080_02 values(3,3);
select pg_sleep(4);
insert into t_timecapsule_0080_01 select 2, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step7: 更新表数据后向t_timecapsule_0080_01插入记录; expect:表结构改变成功且记录插入成功
update t_timecapsule_0080_02 set classno = classno*2;
update t_timecapsule_0080_02 set classno = classno*2;
update t_timecapsule_0080_02 set classno = classno*2;
select pg_sleep(4);
insert into t_timecapsule_0080_01 select 3, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step8: 向表t_timecapsule_0080_02插入数据后向t_timecapsule_0080_01中插入记录; expect:插入成功
insert into t_timecapsule_0080_02 values(1,1);
insert into t_timecapsule_0080_02 values(2,2);
insert into t_timecapsule_0080_02 values(3,3);
select pg_sleep(4);
insert into t_timecapsule_0080_01 select 4, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step9: 清空表数据后向t_timecapsule_0080_01中插入记录; expect:表数据清空成功且插入成功
delete from t_timecapsule_0080_02 where stuno = 1;
delete from t_timecapsule_0080_02 where stuno = 2;
delete from t_timecapsule_0080_02 where stuno = 3;
select pg_sleep(4);
insert into t_timecapsule_0080_01 select 5, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step10: vacuum full表后向t_timecapsule_0080_01中插入记录; expect:vacuum full表成功且插入成功
vacuum full t_timecapsule_0080_02;
select pg_sleep(4);
insert into t_timecapsule_0080_01 select 6, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step10: 创建函数f_timecapsule_0080_01(); expect:函数创建成功
create or replace function f_timecapsule_0080_01(int8)
  returns integer
  language plpgsql
as
$body$
declare
  count integer;
begin
  count = (select snapcsn from t_timecapsule_0080_01 where id =  $1);
  return count;
end;
$body$;
/
--step11: 创建函数f_timecapsule_0080_02(); expect:函数创建成功
create or replace function f_timecapsule_0080_02(int8)
  returns timestamptz
  language plpgsql
as
$body$
declare
  count timestamptz;
begin
  count = (select snaptime from t_timecapsule_0080_01 where id =  $1);
  return count;
end;
$body$;
/
--step12: 对表执行vacuum full后执行闪回及闪回查询; expect:合理报错
timecapsule table t_timecapsule_0080_02 to csn f_timecapsule_0080_01(1);
select * from t_timecapsule_0080_02 timecapsule csn f_timecapsule_0080_01(1) order by stuno;
timecapsule table t_timecapsule_0080_02 to csn f_timecapsule_0080_01(2);
select * from t_timecapsule_0080_02 timecapsule csn f_timecapsule_0080_01(2) order by stuno;
timecapsule table t_timecapsule_0080_02 to csn f_timecapsule_0080_01(3);
select * from t_timecapsule_0080_02 timecapsule csn f_timecapsule_0080_01(3) order by stuno;
timecapsule table t_timecapsule_0080_02 to csn f_timecapsule_0080_01(4);
select * from t_timecapsule_0080_02 timecapsule csn f_timecapsule_0080_01(4) order by stuno;
timecapsule table t_timecapsule_0080_02 to csn f_timecapsule_0080_01(5);
select * from t_timecapsule_0080_02 timecapsule csn f_timecapsule_0080_01(5) order by stuno;

--step13: 对表未执行vacuum full执行闪回及闪回查询; expect:闪回及闪回成功
timecapsule table t_timecapsule_0080_02 to csn f_timecapsule_0080_01(6);
select * from t_timecapsule_0080_02 timecapsule csn f_timecapsule_0080_01(6) order by stuno;

--step14: 清理环境 expect:环境清理成功
drop table if exists t_timecapsule_0080_02;
drop table if exists t_timecapsule_0080_01;
drop function if exists f_timecapsule_0080_02();
drop function if exists f_timecapsule_0080_01();
purge recyclebin;

--step15: 恢复默认值; expect:恢复成功，依次显示结果为off/0/0
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;
alter system set vacuum_defer_cleanup_age to 0;
select pg_sleep(2);
show vacuum_defer_cleanup_age;
alter system set version_retention_age to 0;
select pg_sleep(2);
show version_retention_age;