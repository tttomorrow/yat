-- @testpoint: csn,timestamp闪回及查询语法测试,合理报错

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

--step4: 创建表; expect:表创建成功
drop table if exists t_timecapsule_0070_01;
drop table if exists t_timecapsule_0070_02;
create table t_timecapsule_0070_01(a int);
create table t_timecapsule_0070_02(a int);
select pg_sleep(4);

--step5: 闪回多个对象; expect:闪回失败,合理报错
timecapsule table t_timecapsule_0070_01, t_timecapsule_0070_02 to timestamp now();

--step6: 序列号csn未使用单引号; expect:闪回失败,合理报错
timecapsule table t_timecapsule_0070_01 to csn 92233720368547758;

--step7: 序列号为无效值; expect:闪回失败,合理报错
timecapsule table t_timecapsule_0070_01 to csn '92233720368547758';

--step8: 序列号为表达式; expect:闪回失败,合理报错
timecapsule table t_timecapsule_0070_01 to csn '92233720368547758'+'434';

--step9: csn闪回语句语法错误; expect:闪回失败,合理报错
timecapsule table t_timecapsule_0070_01 to 92233720368547758;
timecapsule table t_timecapsule_0070_01 csn 92233720368547758;

--step10: 正确的timestamp闪回语法; expect:闪回成功
timecapsule table t_timecapsule_0070_01 to timestamp now();

--step11: 查询闪回后的表; expect:显示结果为空与预期结果一致
select * from t_timecapsule_0070_01;

--step12: timestamp闪回语句语法错误; expect:闪回失败,合理报错
timecapsule table t_timecapsule_0070_01 to now();
timecapsule table t_timecapsule_0070_01 timestamp now();

--step13: csn闪回查询csn序列值无效; expect:闪回失败,合理报错
select * from t_timecapsule_0070_01 timecapsule csn (92233720368547758+1111);
select * from t_timecapsule_0070_01 timecapsule csn :p1;
select * from t_timecapsule_0070_01 timecapsule csn (select 1 );
select * from t_timecapsule_0070_01 t timecapsule csn t.a;
select * from t_timecapsule_0070_01 t timecapsule csn constVal();

--step14: csn闪回语句语法错误; expect:闪回失败,合理报错
timecapsule table t_timecapsule_0070_01 to csn (92233720368547758+1111);
timecapsule table t_timecapsule_0070_01 to :p1;

--step15: csn闪回csn序列值无效; expect:闪回失败,合理报错
timecapsule table t_timecapsule_0070_01 csn (select 1 );
timecapsule table t_timecapsule_0070_01 csn (select count(*) from pg_class);

--step16: 清理环境 expect:环境清理成功
drop table if exists t_timecapsule_0070_01;
drop table if exists t_timecapsule_0070_02;
purge recyclebin;

--step17: 恢复默认值; expect:恢复成功，依次显示结果为off/0/0
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;
alter system set vacuum_defer_cleanup_age to 0;
select pg_sleep(2);
show vacuum_defer_cleanup_age;
alter system set version_retention_age to 0;
select pg_sleep(2);
show version_retention_age;