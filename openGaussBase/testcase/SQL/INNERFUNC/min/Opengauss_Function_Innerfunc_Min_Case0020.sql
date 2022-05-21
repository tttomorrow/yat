-- @testpoint: cidr类型取最小值，结果类型转换

--step1:创建表; expect:成功
drop table if exists t_min_case0020;
create table t_min_case0020(c cidr);
create table t_min_case0020_text(t text);
create table t_min_case0020_clob(c clob);
create table t_min_case0020_varchar(c varchar);
create table t_min_case0020_bpchar(c bpchar);
create table t_min_case0020_nvarchar2(c nvarchar2);
create table t_min_case0020_inet(c inet);

--step2:输出转换为text; expect:192.168/24
insert into t_min_case0020 values('192.168/24'),('192.168/25'),('192.168.1'),('192.168');
insert into t_min_case0020_text select min(c) from  t_min_case0020;
select * from  t_min_case0020_text;

--step3:输出转换为clob; expect:192.168/14
delete from t_min_case0020;
insert into t_min_case0020 values('192.168'),('192.168/14');
insert into t_min_case0020_clob select min(c) from  t_min_case0020;
select * from  t_min_case0020_clob;

--step4:输出转换为varchar; expect:9.8
delete from t_min_case0020;
insert into t_min_case0020 values('10'),('9.8'),('10.1');
insert into t_min_case0020_varchar select min(c) from  t_min_case0020;
select * from  t_min_case0020_varchar;

--step5:输出转换为bpchar; expect:192.168.100.128/25
delete from t_min_case0020;
insert into t_min_case0020 values('192.168.100.128/25'),('192.168.100.128');
insert into t_min_case0020_bpchar select min(c) from  t_min_case0020;
select * from  t_min_case0020_bpchar;

--step6:输出转换为nvarchar2; expect:10.1.2.3/32
delete from t_min_case0020;
insert into t_min_case0020 values('10.1.2.3/32'),('10.1.2.12'),('10.1.2.12/30');
insert into t_min_case0020_nvarchar2 select min(c) from  t_min_case0020;
select * from  t_min_case0020_nvarchar2;

--step7:输出转换为inet; expect:10.1.2.3/32
delete from t_min_case0020;
insert into t_min_case0020 values('10.1.2.3/32'),('10.1.2.12/31'),('10.1.2.12/30');
insert into t_min_case0020_inet select min(c) from  t_min_case0020;
select * from  t_min_case0020_inet;

--tearDown
drop table if exists t_min_case0020;
drop table if exists t_min_case0020_text;
drop table if exists t_min_case0020_clob;
drop table if exists t_min_case0020_varchar;
drop table if exists t_min_case0020_bpchar;
drop table if exists t_min_case0020_nvarchar2;
drop table if exists t_min_case0020_inet;