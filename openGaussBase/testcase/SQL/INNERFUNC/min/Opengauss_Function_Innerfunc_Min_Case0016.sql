-- @testpoint: min输入存在空值

--step1:创建表; expect:成功
drop table if exists t_min_case0016;
create table t_min_case0016(c cidr, i inet);

--step2:插入数据; expect:空
insert into t_min_case0016 values(NULL, NULL);
select min(c) from  t_min_case0016;
select min(i) from  t_min_case0016;

--step3:插入数据; expect:255.255.255.1
insert into t_min_case0016 values('255.255.255.1/32', '255.255.255.1/32');
select min(c) from  t_min_case0016;
select min(i) from  t_min_case0016;

--step4:插入数据; expect:0.0.0.0
insert into t_min_case0016 values('0.0.0.0', '0.0.0.0');
select min(c) from  t_min_case0016;
select min(i) from  t_min_case0016;

--step5:插入数据; expect:ffff::ffff
delete from t_min_case0016;
insert into t_min_case0016 values(NULL, NULL),('ffff::ffff/128', 'ffff::ffff/128');
select min(c) from  t_min_case0016;
select min(i) from  t_min_case0016;

--step6:插入数据; expect:::
insert into t_min_case0016 values(NULL, NULL),('::', '::');
select min(c) from  t_min_case0016;
select min(i) from  t_min_case0016;

--tearDown
drop table if exists t_min_case0016;