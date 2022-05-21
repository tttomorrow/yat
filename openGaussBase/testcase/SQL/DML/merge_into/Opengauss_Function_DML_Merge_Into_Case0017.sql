-- @testpoint: 目标表为闪回表，进行merge into操作
--step1: 查询enable_recyclebin默认值; expect:显示默认值off
show enable_recyclebin;
--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
--step3: 清除回收站; expect:回收站清除成功
purge recyclebin;
--step4: 创建目标表和源表并插入数据; expect: 成功
drop table if exists t_mergeinto_17_01;
drop table if exists t_mergeinto_17_02;
create table t_mergeinto_17_01(product_id integer,product_name varchar2(60),
category varchar2(60));
insert into t_mergeinto_17_01 values (1501, 'vivitar 35mm', 'electrncs');
insert into t_mergeinto_17_01 values (1502, 'olympus is50', 'electrncs');
insert into t_mergeinto_17_01 values (1600, 'play gym', 'toys');
insert into t_mergeinto_17_01 values (1601, 'lamaze', 'toys');
insert into t_mergeinto_17_01 values (1666, 'harry potter', 'dvd');
create table t_mergeinto_17_02(product_id integer,product_name varchar2(60),
category varchar2(60));
insert into t_mergeinto_17_02 values (1502, 'olympus camera', 'electrncs');
insert into t_mergeinto_17_02 values (1601, 'lamaze', 'toys');
insert into t_mergeinto_17_02 values (1666, 'harry potter', 'toys');
insert into t_mergeinto_17_02 values (1700, 'wait interface', 'books');
--step5: 查询目标表数据; expect:成功
select * from t_mergeinto_17_01;
--step6: 删除表目标表; expect:表删除成功
drop table t_mergeinto_17_01 cascade;
--step7: 在回收站中统计名称t_mergeinto_17_01和操作类型为drop; expect:预期结果为1
select count(*) from gs_recyclebin where rcyoriginname = 't_mergeinto_17_01' and rcyoperation = 'd';
--step8: 对表目标表执行闪回drop; expect:闪回成功
timecapsule table t_mergeinto_17_01 to before drop;
--step9: 查询闪回后的目标表数据; expect:成功
select * from t_mergeinto_17_01;
--step10: 进行merge into 操作 ;expect: 成功
merge into t_mergeinto_17_01 t1  using  t_mergeinto_17_02  t2
   on (t1.product_id = t2.product_id)
when matched then
  update set t1.product_name = t2.product_name, t1.category = t2.category
  where t1.product_name != 'play gym'
when not matched then
  insert values (t2.product_id, t2.product_name, t2.category)
  where t2.category = 'books';
--step11: 查询更新后的结果 ;expect: 成功
select * from t_mergeinto_17_01 order by product_id;
--step12: 清理环境  ;expect: 成功
drop table t_mergeinto_17_01;
drop table t_mergeinto_17_02;
alter system set enable_recyclebin to off;