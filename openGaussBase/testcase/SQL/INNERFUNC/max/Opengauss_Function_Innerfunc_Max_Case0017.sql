-- @testpoint: ipv4网络地址无子网掩码比大小

--step1:创建表; expect:成功
drop table if exists t_max_case0017;
create table t_max_case0017(c cidr, i inet);

--step2:插入数据; expect:128.255.255.254
insert into t_max_case0017 values('128.255.255.254', '128.255.255.254'),('128.255.255.0', '128.255.255.0');
select max(c) from  t_max_case0017;
select max(i) from  t_max_case0017;

--step3:插入数据; expect:0.0.255.255
delete from t_max_case0017;
insert into t_max_case0017 values('0.0.255.0', '0.0.255.0'),('0.0.255.255', '0.0.255.255');
select max(c) from  t_max_case0017;
select max(i) from  t_max_case0017;

--tearDown
drop table if exists t_max_case0017;