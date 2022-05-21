-- @testpoint: max输入存在空值

--step1:创建表; expect:成功
drop table if exists t_max_case0027;
create table t_max_case0027(c cidr, i inet);

--step2:插入数据; expect:空
insert into t_max_case0027 values(NULL, NULL);
select max(c) from  t_max_case0027;
select max(i) from  t_max_case0027;

--step3:插入数据; expect:0.0.0.0
insert into t_max_case0027 values('0.0.0.0', '0.0.0.0');
select max(c) from  t_max_case0027;
select max(i) from  t_max_case0027;

--step4:插入数据; expect:255.255.255.1
insert into t_max_case0027 values('255.255.255.1/32', '255.255.255.1/32');
select max(c) from  t_max_case0027;
select max(i) from  t_max_case0027;

--step5:插入数据; expect:::
delete from t_max_case0027;
insert into t_max_case0027 values(NULL, NULL),('::', '::');
select max(c) from  t_max_case0027;
select max(i) from  t_max_case0027;

--step6:插入数据; expect:ffff::ffff
insert into t_max_case0027 values(NULL, NULL),('ffff::ffff/128', 'ffff::ffff/128');
select max(c) from  t_max_case0027;
select max(i) from  t_max_case0027;

--tearDown
drop table if exists t_max_case0027;