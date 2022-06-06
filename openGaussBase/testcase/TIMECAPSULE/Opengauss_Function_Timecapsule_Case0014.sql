-- @testpoint: 调用函数清除回收站中指定的表

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清除回收站; expect:回收站清除成功
drop table if exists t_timecapsule_0014;
purge recyclebin;

--step4: 创建表、插入数据并删除表; expect:表创建成功、数据插入成功且表删除
create table t_timecapsule_0014(a int);
insert into t_timecapsule_0014 values(1);
drop table t_timecapsule_0014;

--step5: 创建表、插入数据并删除表; expect:表创建成功、数据插入成功且表删除
create table t_timecapsule_0014(a int);
insert into t_timecapsule_0014 values(2);
drop table t_timecapsule_0014;

--step6: 创建表、插入数据并删除表; expect:表创建成功、数据插入成功且表删除
create table t_timecapsule_0014(a int);
insert into t_timecapsule_0014 values(3);
drop table t_timecapsule_0014;

--step7: 创建函数f_timecapsule_0014_01(); expect:函数创建成功
drop function if exists f_timecapsule_0014_01();
create or replace function f_timecapsule_0014_01(varchar, varchar)
  returns varchar
  language plpgsql
as
$body$
declare
  sqltext text;
begin
  sqltext = 'purge '|| $1 ||' "' || $2 ||'"';
  execute sqltext;
  return 0;
end;
$body$;
/

--step8: 创建函数f_timecapsule_0014_02(); expect:函数创建成功
drop function if exists f_timecapsule_0014_02();
create or replace function f_timecapsule_0014_02(varchar, char, int8)
  returns varchar
  language plpgsql
as
$body$
declare
  ret varchar;
begin
  ret = (select t.rcyname from gs_recyclebin t where t.rcyoriginname = $1 and t.rcyoperation=$2 order by t.rcychangecsn asc offset ($3 -1 ) limit 1);
  return ret;
end;
$body$;
/

--step9: 调用函数删除回收站中指定表; expect:表删除成功,返回结果为0
select f_timecapsule_0014_01('table', f_timecapsule_0014_02('t_timecapsule_0014', 'd', 3));

--step10: 在回收站中统计删除的表 expect:统计结果为2条数据
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0014' and rcyoperation = 'd';

--step15: 调用函数删除回收站中指定表; expect:表删除成功,返回结果为0
select f_timecapsule_0014_01('table', f_timecapsule_0014_02('t_timecapsule_0014', 'd', 2));

--step16: 在回收站中统计删除的表 expect:统计结果为1条数据
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0014' and rcyoperation = 'd';

--step17: 执行闪回; expect:闪回成功
timecapsule table t_timecapsule_0014 to before drop;

--step18: 查询闪回后的表 expect:查询结果为数据1与预期结果一致
select * from t_timecapsule_0014;

--step16: 在回收站中统计删除的表 expect:统计结果为0条数据
select count(*) from gs_recyclebin where rcyoriginname = 't_timecapsule_0014' and rcyoperation = 'd';

--step17: 清理环境 expect:环境清理成功
drop function if exists f_timecapsule_0014_01();
drop function if exists f_timecapsule_0014_02();
drop table if exists t_timecapsule_0014 purge;
purge recyclebin;

--step18: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;