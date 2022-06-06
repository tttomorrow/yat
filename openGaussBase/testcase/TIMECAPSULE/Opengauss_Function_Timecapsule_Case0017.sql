-- @testpoint: 调用函数执行truncate闪回

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清除回收站; expect:回收站清除成功
drop table if exists t_timecapsule_0017;
purge recyclebin;

--step4: 创建表; expect:表创建成功
create table t_timecapsule_0017(a int, b int);

--step5: 向表中插入数据; expect:数据插入成功
insert into t_timecapsule_0017 values(1);
insert into t_timecapsule_0017 values(2);
insert into t_timecapsule_0017 values(3);

--step6: 清空表数据; expect:表数据清空成功
truncate table t_timecapsule_0017;

--step7: 在回收站中统计删除的表 expect:统计结果为1条数据
select count(*) from gs_recyclebin where rcyoriginname like 't_timecapsule_0017' and rcyoperation = 't';

--step8: 创建函数f_timecapsule_0017_01(); expect:函数创建成功
drop FUNCTION if exists f_timecapsule_0017_01();
CREATE OR REPLACE FUNCTION f_timecapsule_0017_01(varchar, varchar)
  RETURNS varchar
  LANGUAGE plpgsql
AS
$BODY$
declare
  sqlText text;
begin
  sqlText = 'timecapsule '|| $1 ||' "' || $2 ||'" to before truncate';
  execute sqlText;
  return 0;
end;
$BODY$;
/
--step9: 创建函数f_timecapsule_0017_02(); expect:函数创建成功
drop FUNCTION if exists f_timecapsule_0017_02();
CREATE OR REPLACE FUNCTION f_timecapsule_0017_02(varchar, char, int8)
  RETURNS varchar
  LANGUAGE plpgsql
AS
$BODY$
declare
  ret varchar;
begin
  ret = (select t.rcyname from gs_recyclebin t where t.rcyoriginname = $1 and t.rcyoperation=$2 order by t.rcychangecsn asc offset ($3 -1 ) limit 1);
  return ret;
end;
$BODY$;
/
--step10: 调用函数删除执行闪回; expect:闪回成功,返回结果为0
select f_timecapsule_0017_01('table',f_timecapsule_0017_02('t_timecapsule_0017', 't', 1));

--step11: 查询闪回后的表 expect:查询到表中的数据有3条数据与预期结果一致
select * from t_timecapsule_0017;

--step12: 清空回收站; expect:回收站清空成功
purge recyclebin;

--step13: 清空回收站中表数据; expect:表数据清空成功
truncate table t_timecapsule_0017 purge;

--step14: 在回收站中统计删除的表 expect:统计结果为0条数据
select count(*) from gs_recyclebin where rcyoriginname like 't_timecapsule_0017' and rcyoperation = 't';

--step15: 清理环境 expect:环境清理成功
drop function if exists f_timecapsule_0017_01();
drop function if exists f_timecapsule_0017_02();
drop table if exists t_timecapsule_0017 purge;
purge recyclebin;

--step16: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;