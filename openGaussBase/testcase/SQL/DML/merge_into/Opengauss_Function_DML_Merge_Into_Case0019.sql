-- @testpoint: 目标表为二级分区表，进行merge into操作，合理报错
--step1: 创建目标表和源表并插入数据; expect: 成功
drop table if exists t_mergeinto_19_01;
drop table if exists t_mergeinto_19_02;
create table t_mergeinto_19_01(product_id integer,product_name varchar2(60),
category varchar2(60))
  partition by list(category) subpartition by range(product_id )
(
  partition p_electrncs VALUES ( 'electrncs' )(
    subpartition electrncs_1 values less than(1502),
    subpartition electrncs_2 values less than(1503)),
  partition p_toys VALUES ( 'toys' )(
    subpartition toys_1 values less than(1600),
    subpartition toys_2 values less than(1602))
);
insert into t_mergeinto_19_01 values (1501, 'vivitar 35mm', 'electrncs');
insert into t_mergeinto_19_01 values (1502, 'olympus is50', 'electrncs');
insert into t_mergeinto_19_01 values (1600, 'play gym', 'toys');
insert into t_mergeinto_19_01 values (1601, 'lamaze', 'toys');
create table t_mergeinto_19_02(product_id integer,product_name varchar2(60),
category varchar2(60));
insert into t_mergeinto_19_02 values (1502, 'olympus camera', 'electrncs');
insert into t_mergeinto_19_02 values (1601, 'lamaze', 'toys');
insert into t_mergeinto_19_02 values (1666, 'harry potter', 'toys');
insert into t_mergeinto_19_02 values (1700, 'wait interface', 'books');
--step2: 进行merge into 操作 ;expect: 失败
merge into t_mergeinto_19_01 t1  using  t_mergeinto_19_02  t2
   on (t1.product_id = t2.product_id)
when matched then
  update set t1.product_name = t2.product_name, t1.category = t2.category
  where t1.product_name != 'play gym'
when not matched then
  insert values (t2.product_id, t2.product_name, t2.category)
  where t2.category = 'books';
--step3: 查询结果不变 ;expect: 成功
select * from t_mergeinto_19_01 order by product_id;
--step4: 清理环境  ;expect: 成功
drop table t_mergeinto_19_01;
drop table t_mergeinto_19_02;
