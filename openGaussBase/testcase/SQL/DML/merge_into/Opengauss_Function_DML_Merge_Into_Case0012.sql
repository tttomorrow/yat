-- @testpoint: 目标表为系统表，进行merge into操作,合理报错
--step1: 创建源表并插入数据;expect: 成功
drop table if exists t_mergeinto_12_01;
create table t_mergeinto_12_01(product_id integer,product_name varchar2(60),
category varchar2(60));
insert into t_mergeinto_12_01 values (1502, 'olympus camera', 'electrncs');
insert into t_mergeinto_12_01 values (1601, 'lamaze', 'toys');
insert into t_mergeinto_12_01 values (1666, 'harry potter', 'toys');
insert into t_mergeinto_12_01 values (1700, 'wait interface', 'books');
--step2: 进行merge into 操作 ;expect: 失败
merge into  pg_user p using t_mergeinto_12_01 t1
on (p.usesysid = t1.product_id)
when matched then
  update set p.usename = t1.product_name;
--step3: 清理环境删除表 ; expect: 成功
drop table t_mergeinto_12_01;