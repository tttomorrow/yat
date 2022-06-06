-- @testpoint: ipv6网络地址无子网掩码比大小取最小值

--step1:创建表; expect:成功
drop table if exists t_min_case0009;
create table t_min_case0009(c cidr, i inet);

--step2:插入数据; expect:::fe:c0A8:0001
insert into t_min_case0009 values('::fe:192.168.0.1', '::fe:192.168.0.1'),('::fe:c0A8:0001', '::fe:c0A8:0001');
select min(c) from  t_min_case0009;
select min(i) from  t_min_case0009;

--step3:插入数据; expect:::fe:c0A8:1
delete from t_min_case0009;
insert into t_min_case0009 values('::fe:192.168.0.2', '::fe:192.168.0.2'),('::fe:c0A8:0001', '::fe:c0A8:0001');
select min(c) from  t_min_case0009;
select min(i) from  t_min_case0009;

--step4:插入数据; expect:::FFFf:0
delete from t_min_case0009;
insert into t_min_case0009 values('::FFFf:0', '::FFFf:0'),('::FFFf:255.255.255.255', '::FFFf:255.255.255.255');
select min(c) from  t_min_case0009;
select min(i) from  t_min_case0009;

--tearDown
drop table if exists t_min_case0009;