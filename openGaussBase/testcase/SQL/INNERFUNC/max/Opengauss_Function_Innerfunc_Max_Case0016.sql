-- @testpoint: cidr类型网络地址/子网掩码/主机地址组合测试--ipv4

--step1:创建表; expect:成功
drop table if exists t_max_case0016;
create table t_max_case0016(id int, c cidr);

--step2:主机地址不同; expect:122.5.5.9
insert into t_max_case0016 values(1,'122.5.5.3/32'),(2,'122.5.5.9/32');
select max(c) from  t_max_case0016;

--step3:子网掩码不同，长度相同部分网络地址不同; expect:128.224.0.0/11
delete from t_max_case0016;
insert into t_max_case0016 values(1,'128.224.0.0/11'),(2,'128.192.252.0/22');
select max(c) from  t_max_case0016;

--step4:子网掩码不同:长度相同部分网络地址同; expect:128.224.252.0/22
delete from t_max_case0016;
insert into t_max_case0016 values(1,'128.224.0.0/11'),(2,'128.224.252.0/22');
select max(c) from  t_max_case0016;

--step5:子网掩码相同:网络地址不同，; expect:129.255.224.0/19
delete from t_max_case0016;
insert into t_max_case0016 values(1,'128.255.192.0/19'),(2,'128.255.224.0/19');
select max(c) from  t_max_case0016;

--step6:全1地址与全0地址; expect:255.255.255.255
delete from t_max_case0016;
insert into t_max_case0016 values(1,'255.255.255.255'),(2,'0.0.0.0');
select max(c) from  t_max_case0016;

--step7:子网掩码不同:网络地址相同; expect:128.224.0.0/22
delete from t_max_case0016;
insert into t_max_case0016 values(1,'128.224.0.0/11'),(2,'128.224.0.0/22');
select max(c) from  t_max_case0016;

--tearDown
drop table if exists t_max_case0016;