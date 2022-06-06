-- @testpoint: csn,timestamp闪回查询与其他DML语句混合测试

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

--step4: 创建表t_timecapsule_0066_01; expect:表创建成功
drop table if exists t_timecapsule_0066_01;
create table t_timecapsule_0066_01(id int, snaptime timestamptz, snapcsn bigint);

--step5: 创建表t_timecapsule_0066_02后向t_timecapsule_0066_01中插入记录; expect:表创建成功且记录插入成功
create table t_timecapsule_0066_02(a int);
select pg_sleep(4);
insert into t_timecapsule_0066_01 select 1, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step6: 向表t_timecapsule_0066_02插入数据后向t_timecapsule_0066_01中插入记录; expect:插入成功
insert into t_timecapsule_0066_02 values(1),(2),(3);
select pg_sleep(4);
insert into t_timecapsule_0066_01 select 2, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step7: 更新表t_timecapsule_0066_02值后向t_timecapsule_0066_01中插入记录; expect:插入成功
update t_timecapsule_0066_02 set a = 99 where a = 2;
select pg_sleep(4);
insert into t_timecapsule_0066_01 select 3, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step8: 清空表t_timecapsule_0066_02中一条数据后向t_timecapsule_0066_01中插入记录; expect:插入成功
delete from t_timecapsule_0066_02 where a = 3;
select pg_sleep(4);
insert into t_timecapsule_0066_01 select 4, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step9: 创建表t_timecapsule_0066_02后向t_timecapsule_0066_01中插入记录; expect:表创建成功且记录插入成功
insert into t_timecapsule_0066_02 values(4),(5);
select pg_sleep(4);
insert into t_timecapsule_0066_01 select 5, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step10: 创建函数f_timecapsule_0066_01(); expect:函数创建成功
create or replace function f_timecapsule_0066_01(int8)
  returns integer
  language plpgsql
as
$body$
declare
  count integer;
begin
  count = (select snapcsn from t_timecapsule_0066_01 where id =  $1);
  return count;
end;
$body$;
/
--step11: 创建函数f_timecapsule_0066_02(); expect:函数创建成功
create or replace function f_timecapsule_0066_02(int8)
  returns timestamptz
  language plpgsql
as
$body$
declare
  count timestamptz;
begin
  count = (select snaptime from t_timecapsule_0066_01 where id =  $1);
  return count;
end;
$body$;
/
--step12: CSN闪回查询与UPDATE语句混合; expect:update数据成功
update t_timecapsule_0066_02 set a = 100 where a in ( select a from t_timecapsule_0066_02 timecapsule csn f_timecapsule_0066_01(2)) and a in ( select a from t_timecapsule_0066_02 timecapsule csn f_timecapsule_0066_01(5));
update t_timecapsule_0066_02 set a = 101 where a in ( select a from t_timecapsule_0066_02 timecapsule csn f_timecapsule_0066_01(3)) and a in ( select a from t_timecapsule_0066_02 timecapsule csn f_timecapsule_0066_01(4));
update t_timecapsule_0066_02 set a = 102 where a in ( select a from t_timecapsule_0066_02 timecapsule csn f_timecapsule_0066_01(4)) and a in ( select a from t_timecapsule_0066_02 timecapsule csn f_timecapsule_0066_01(3));
update t_timecapsule_0066_02 set a = 103 where a in ( select a from t_timecapsule_0066_02 timecapsule csn f_timecapsule_0066_01(5)) and a in ( select a from t_timecapsule_0066_02 timecapsule csn f_timecapsule_0066_01(2));

--step13: 查询表数据; expect:查询结果与update后一致
select * from  t_timecapsule_0066_02;

--step14: CSN闪回查询与delete语句混合; expect:delete数据成功
delete from t_timecapsule_0066_02 where a in ( select a from t_timecapsule_0066_02 timecapsule csn f_timecapsule_0066_01(2)) and a in ( select a from t_timecapsule_0066_02 timecapsule csn f_timecapsule_0066_01(5));
delete from t_timecapsule_0066_02 where a in ( select a from t_timecapsule_0066_02 timecapsule csn f_timecapsule_0066_01(3)) and a in ( select a from t_timecapsule_0066_02 timecapsule csn f_timecapsule_0066_01(4));
delete from t_timecapsule_0066_02 where a in ( select a from t_timecapsule_0066_02 timecapsule csn f_timecapsule_0066_01(4)) and a in ( select a from t_timecapsule_0066_02 timecapsule csn f_timecapsule_0066_01(3));
delete from t_timecapsule_0066_02 where a in ( select a from t_timecapsule_0066_02 timecapsule csn f_timecapsule_0066_01(5)) and a in ( select a from t_timecapsule_0066_02 timecapsule csn f_timecapsule_0066_01(2));

--step15: 查询表数据; expect:查询结果与delete后一致
select * from  t_timecapsule_0066_02;

--step16: CSN闪回查询与insert语句混合; expect:insert数据成功
insert into t_timecapsule_0066_02 select * from t_timecapsule_0066_02 timecapsule csn f_timecapsule_0066_01(2);
insert into t_timecapsule_0066_02 select * from t_timecapsule_0066_02 timecapsule csn f_timecapsule_0066_01(3);
insert into t_timecapsule_0066_02 select * from t_timecapsule_0066_02 timecapsule csn f_timecapsule_0066_01(4);
insert into t_timecapsule_0066_02 select * from t_timecapsule_0066_02 timecapsule csn f_timecapsule_0066_01(5);

--step17: 查询表数据; expect:查询结果与insert数据后一致
select * from  t_timecapsule_0066_02;

--step18: timestamp闪回查询与insert语句混合; expect:insert数据成功
insert into t_timecapsule_0066_02 select * from t_timecapsule_0066_02 timecapsule timestamp f_timecapsule_0066_02(2);
insert into t_timecapsule_0066_02 select * from t_timecapsule_0066_02 timecapsule timestamp f_timecapsule_0066_02(3);
insert into t_timecapsule_0066_02 select * from t_timecapsule_0066_02 timecapsule timestamp f_timecapsule_0066_02(4);
insert into t_timecapsule_0066_02 select * from t_timecapsule_0066_02 timecapsule timestamp f_timecapsule_0066_02(5);

--step19: 查询表数据; expect:查询结果与insert后一致
select * from  t_timecapsule_0066_02;

--step20: 清理环境 expect:环境清理成功
drop table if exists t_timecapsule_0066_02;
drop table if exists t_timecapsule_0066_01;
drop function if exists f_timecapsule_0066_02();
drop function if exists f_timecapsule_0066_01();
purge recyclebin;

--step21: 恢复默认值; expect:恢复成功，依次显示结果为off/0/0
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;
alter system set vacuum_defer_cleanup_age to 0;
select pg_sleep(2);
show vacuum_defer_cleanup_age;
alter system set version_retention_age to 0;
select pg_sleep(2);
show version_retention_age;