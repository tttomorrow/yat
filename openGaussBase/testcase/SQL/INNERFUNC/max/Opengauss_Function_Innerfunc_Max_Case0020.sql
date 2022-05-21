-- @testpoint: ipv6网络地址无子网掩码比大小

--step1:创建表; expect:成功
drop table if exists t_max_case0020;
create table t_max_case0020(c cidr, i inet);

--step2:插入数据; expect:::fe:c0A8:0001
insert into t_max_case0020 values('::fe:192.168.0.1', '::fe:192.168.0.1'),('::fe:c0A8:0001', '::fe:c0A8:0001');
select max(c) from  t_max_case0020;
select max(i) from  t_max_case0020;

--step3:插入数据; expect:::fe:c0a8:2
delete from t_max_case0020;
insert into t_max_case0020 values('::fe:192.168.0.2', '::fe:192.168.0.2'),('::fe:c0A8:0001', '::fe:c0A8:0001');
select max(c) from  t_max_case0020;
select max(i) from  t_max_case0020;

--step4:插入数据; expect:::ffff:255.255.255.255
delete from t_max_case0020;
insert into t_max_case0020 values('::FFFf:0', '::FFFf:0'),('::FFFf:255.255.255.255', '::FFFf:255.255.255.255');
select max(c) from  t_max_case0020;
select max(i) from  t_max_case0020;

--tearDown
drop table if exists t_max_case0020;