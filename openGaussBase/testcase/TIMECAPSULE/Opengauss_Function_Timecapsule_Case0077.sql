-- @testpoint: 不支持csn闪回带外键的表,合理报错

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

--step4: 创建主外键表并向主键表中插入数据; expect:表创建成功且数据插入成功
create table t_timecapsule_0077_01
(
    w_city            varchar(60)                primary key,
    w_address       text
);

create table t_timecapsule_0077_02
(
    w_warehouse_sk            integer               not null,
    w_warehouse_id            char(16)              not null,
    w_warehouse_name          varchar(20)                   ,
    w_suite_number            char(10)                      ,
    w_city                    varchar(60)           references t_timecapsule_0077_01(w_city)
);

--step5: 创建表t_timecapsule_0077_03; expect:表创建成功
drop table if exists t_timecapsule_0077_03;
create table t_timecapsule_0077_03(id int, snaptime timestamptz, snapcsn bigint);

insert into t_timecapsule_0077_01 values('xian', '环普科技园');
--step6: 向外键表t_timecapsule_0077_02插入数据后向t_timecapsule_0077_03中插入记录; expect:插入成功
insert into t_timecapsule_0077_02 values(1, '1001', '环普', '320001', 'xian');
select pg_sleep(4);
insert into t_timecapsule_0077_03 select 1, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

insert into t_timecapsule_0077_02 values(2, '1002', '环普', '320002', 'xian');
select pg_sleep(4);
insert into t_timecapsule_0077_03 select 2, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

insert into t_timecapsule_0077_02 values(3, '1003', '环普', '320003', 'xian');
select pg_sleep(4);
insert into t_timecapsule_0077_03 select 3, now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();

--step7: 创建函数f_timecapsule_0077_01(); expect:函数创建成功
create or replace function f_timecapsule_0077_01(int8)
  returns integer
  language plpgsql
as
$body$
declare
  count integer;
begin
  count = (select snapcsn from t_timecapsule_0077_03 where id =  $1);
  return count;
end;
$body$;
/
--step8: 创建函数f_timecapsule_0077_02(); expect:函数创建成功
create or replace function f_timecapsule_0077_02(int8)
  returns timestamptz
  language plpgsql
as
$body$
declare
  count timestamptz;
begin
  count = (select snaptime from t_timecapsule_0077_03 where id =  $1);
  return count;
end;
$body$;
/
--step9: 执行闪回; expect:闪回失败,合理报错
timecapsule table t_timecapsule_0077_02 to csn f_timecapsule_0077_01(1);
timecapsule table t_timecapsule_0077_02 to csn f_timecapsule_0077_01(2);
timecapsule table t_timecapsule_0077_02 to csn f_timecapsule_0077_01(3);

--step10: 执行闪回查询; expect:查询成功
select * from t_timecapsule_0077_02 timecapsule csn f_timecapsule_0077_01(1) order by w_warehouse_sk;
select * from t_timecapsule_0077_02 timecapsule csn f_timecapsule_0077_01(2) order by W_WAREHOUSE_SK;
select * from t_timecapsule_0077_02 timecapsule csn f_timecapsule_0077_01(3) order by W_WAREHOUSE_SK;

--step11: 清理环境 expect:环境清理成功
drop table if exists t_timecapsule_0077_02;
drop table if exists t_timecapsule_0077_01;
drop table if exists t_timecapsule_0077_03;
drop function if exists f_timecapsule_0077_02();
drop function if exists f_timecapsule_0077_01();
purge recyclebin;

--step12: 恢复默认值; expect:恢复成功，依次显示结果为off/0/0
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;
alter system set vacuum_defer_cleanup_age to 0;
select pg_sleep(2);
show vacuum_defer_cleanup_age;
alter system set version_retention_age to 0;
select pg_sleep(2);
show version_retention_age;