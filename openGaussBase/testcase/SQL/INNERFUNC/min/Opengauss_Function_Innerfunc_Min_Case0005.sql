-- @testpoint: cidr类型网络地址/子网掩码/主机地址组合测试取最小值--ipv4

--step1:创建表; expect:成功
drop table if exists t_min_case0005;
create table t_min_case0005(id int, c cidr);

--step2:主机地址不同; expect:122.5.5.3
insert into t_min_case0005 values(1,'122.5.5.3/32'),(2,'122.5.5.9/32');
select min(c) from  t_min_case0005;

--step3:子网掩码不同，长度相同部分网络地址不同; expect:128.192.252.0/22
delete from t_min_case0005;
insert into t_min_case0005 values(1,'128.224.0.0/11'),(2,'128.192.252.0/22');
select min(c) from  t_min_case0005;

--step4:子网掩码不同:长度相同部分网络地址同; expect:128.224.0.0/11
delete from t_min_case0005;
insert into t_min_case0005 values(1,'128.224.0.0/11'),(2,'128.224.252.0/22');
select min(c) from  t_min_case0005;

--step5:子网掩码相同:网络地址不同，; expect:128.255.192.0/19
delete from t_min_case0005;
insert into t_min_case0005 values(1,'128.255.192.0/19'),(2,'128.255.224.0/19');
select min(c) from  t_min_case0005;

--step6:全1地址与全0地址; expect:0.0.0.0
delete from t_min_case0005;
insert into t_min_case0005 values(1,'255.255.255.255'),(2,'0.0.0.0');
select min(c) from  t_min_case0005;

--step7:子网掩码不同:网络地址相同; expect:128.224.0.0/11
delete from t_min_case0005;
insert into t_min_case0005 values(1,'128.224.0.0/11'),(2,'128.224.0.0/22');
select min(c) from  t_min_case0005;

--tearDown
drop table if exists t_min_case0005;