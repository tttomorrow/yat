-- @testpoint: cidr类型取最大值，结果类型转换

--step1:创建表; expect:成功
drop table if exists t_max_case0031;
create table t_max_case0031(c cidr);
create table t_max_case0031_text(t text);
create table t_max_case0031_clob(c clob);
create table t_max_case0031_varchar(c varchar);
create table t_max_case0031_bpchar(c bpchar);
create table t_max_case0031_nvarchar2(c nvarchar2);
create table t_max_case0031_inet(c inet);

--step2:输出转换为text; expect:192.168.1.0/24
insert into t_max_case0031 values('192.168/24'),('192.168/25'),('192.168.1'),('192.168');
insert into t_max_case0031_text select max(c) from  t_max_case0031;
select * from  t_max_case0031_text;

--step3:输出转换为clob; expect:192.168.0.0/24
delete from t_max_case0031;
insert into t_max_case0031 values('192.168'),('192.168/14');
insert into t_max_case0031_clob select max(c) from  t_max_case0031;
select * from  t_max_case0031_clob;

--step4:输出转换为varchar; expect:10.1.0.0/16
delete from t_max_case0031;
insert into t_max_case0031 values('10'),('9.8'),('10.1');
insert into t_max_case0031_varchar select max(c) from  t_max_case0031;
select * from  t_max_case0031_varchar;

--step5:输出转换为bpchar; expect:192.168.100.128/32
delete from t_max_case0031;
insert into t_max_case0031 values('192.168.100.128/25'),('192.168.100.128');
insert into t_max_case0031_bpchar select max(c) from  t_max_case0031;
select * from  t_max_case0031_bpchar;

--step6:输出转换为nvarchar2; expect:10.1.2.12
delete from t_max_case0031;
insert into t_max_case0031 values('10.1.2.3/32'),('10.1.2.12'),('10.1.2.12/30');
insert into t_max_case0031_nvarchar2 select max(c) from  t_max_case0031;
select * from  t_max_case0031_nvarchar2;

--step7:输出转换为inet; expect:10.1.2.12/31
delete from t_max_case0031;
insert into t_max_case0031 values('10.1.2.3/32'),('10.1.2.12/31'),('10.1.2.12/30');
insert into t_max_case0031_inet select max(c) from  t_max_case0031;
select * from  t_max_case0031_inet;

--tearDown
drop table if exists t_max_case0031;
drop table if exists t_max_case0031_text;
drop table if exists t_max_case0031_clob;
drop table if exists t_max_case0031_varchar;
drop table if exists t_max_case0031_bpchar;
drop table if exists t_max_case0031_nvarchar2;
drop table if exists t_max_case0031_inet;