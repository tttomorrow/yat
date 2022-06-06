-- @testpoint: ipv4网络地址无子网掩码比大小取最小值

--step1:创建表; expect:成功
drop table if exists t_min_case0006;
create table t_min_case0006(c cidr, i inet);

--step2:插入数据; expect:128.255.255.0
insert into t_min_case0006 values('128.255.255.254', '128.255.255.254'),('128.255.255.0', '128.255.255.0');
select min(c) from  t_min_case0006;
select min(i) from  t_min_case0006;

--step3:插入数据; expect:0.0.255.0
delete from t_min_case0006;
insert into t_min_case0006 values('0.0.255.0', '0.0.255.0'),('0.0.255.255', '0.0.255.255');
select min(c) from  t_min_case0006;
select min(i) from  t_min_case0006;

--tearDown
drop table if exists t_min_case0006;