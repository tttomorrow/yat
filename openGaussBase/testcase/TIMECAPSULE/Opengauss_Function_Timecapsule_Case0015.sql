-- @testpoint: 调用函数清除回收站中指定索引,合理报错

--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清除回收站; expect:回收站清除成功
drop table if exists t_timecapsule_0015;
purge recyclebin;

--step4: 创建表; expect:表创建成功
create table t_timecapsule_0015(a int);

--step5: 向表中插入数据; expect:数据插入成功
insert into t_timecapsule_0015 values(1);
insert into t_timecapsule_0015 values(2);
insert into t_timecapsule_0015 values(3);

--step6: 创建索引; expect:索引创建成功
create unique index  i_timecapsule_0015 on t_timecapsule_0015(a);

--step7: 向表中插入已有数据; expect:数据插入失败合理报错
insert into t_timecapsule_0015 values(3);

--step8: 删除表; expect:删除表成功
drop table t_timecapsule_0015;

--step9: 在回收站中统计删除的表 expect:统计结果为2条数据
select count(*) from gs_recyclebin where rcyoriginname like '%_timecapsule_0015%' and rcyoperation = 'd';

--step10: 创建函数f_timecapsule_0015_01(); expect:函数创建成功
drop function if exists f_timecapsule_0015_01();
create or replace function f_timecapsule_0015_01(varchar, varchar)
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

--step11: 创建函数f_timecapsule_0015_02(); expect:函数创建成功
drop function if exists f_timecapsule_0015_02();
create or replace function f_timecapsule_0015_02(varchar, char, int8)
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

--step12: 调用函数删除回收站中指定索引; expect:索引删除成功，返回结果为0
select f_timecapsule_0015_01('index', f_timecapsule_0015_02('i_timecapsule_0015', 'd', 1));

--step13: 在回收站中统计删除的表 expect:统计结果为1条数据
select count(*) from gs_recyclebin where rcyoriginname like '%_timecapsule_0015%' and rcyoperation = 'd';

--step14: 执行闪回; expect:闪回成功
timecapsule table t_timecapsule_0015 to before drop;

--step15: 向表中插入已有数据; expect:数据插入成功
insert into t_timecapsule_0015 values(3);

--step16: 查询闪回后的表 expect:查询到表中的数据有4条数据与预期结果一致
select * from t_timecapsule_0015;

--step17: 清理环境 expect:环境清理成功
drop function if exists f_timecapsule_0015_01();
drop function if exists f_timecapsule_0015_02();
drop table if exists t_timecapsule_0015;
purge recyclebin;

--step18: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;