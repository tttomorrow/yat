-- @testpoint: cidr类型网络地址/子网掩码/主机地址组合测试取最小值--ipv6

--step1:创建表; expect:成功
drop table if exists t_min_case0008;
create table t_min_case0008(id int, c cidr);

--step2:主机地址不同; expect:::fe:c0A8:1
insert into t_min_case0008 values(1,'::fe:192.168.0.1/128'),(2,'::fe:c0A8:0002/128');
select min(c) from  t_min_case0008;

--step3:子网掩码不同，长度相同部分网络地址不同; expect:aa:bb:cc:dd::/115
delete from t_min_case0008;
insert into t_min_case0008 values(1,'aa:bb:cc:dd::/115'),(2,'aa:bb:cc:de::/64');
select min(c) from  t_min_case0008;

--step4:子网掩码不同:长度相同部分网络地址同; expect:aa:bb:cc:de::/63
delete from t_min_case0008;
insert into t_min_case0008 values(1,'aa:bb:cc:df::/115'),(2,'aa:bb:cc:de::/63');
select min(c) from  t_min_case0008;

--step5:子网掩码相同:网络地址不同，; expect:aa:bb:cc:de::/64
delete from t_min_case0008;
insert into t_min_case0008 values(1,'aa:bb:cc:0d0e::/64'),(2,'aa:bb:cc:de::/64');
select min(c) from  t_min_case0008;
--step6:全1地址与全0地址; expect:::
delete from t_min_case0008;
insert into t_min_case0008 values(1,'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'),(2,'::');
select min(c) from  t_min_case0008;

--step7:子网掩码不同:网络地址相同; expect:aa:bb:cc:de::/64
delete from t_min_case0008;
insert into t_min_case0008 values(1,'aa:bb:cc:de::/115'),(2,'aa:bb:cc:de::/64');
select min(c) from  t_min_case0008;

--tearDown
drop table if exists t_min_case0008;