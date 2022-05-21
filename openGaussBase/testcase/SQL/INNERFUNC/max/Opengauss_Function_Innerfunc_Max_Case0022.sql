-- @testpoint: 非网络类型转换为inet后ipv4地址取最大值

--step1:创建表; expect:成功
drop table if exists t_max_case0022;
create table t_max_case0022(c inet);
create table t_max_case0022_text(t text);
create table t_max_case0022_clob(c clob);
create table t_max_case0022_varchar(c varchar);
create table t_max_case0022_bpchar(c bpchar);
create table t_max_case0022_nvarchar2(c nvarchar2);
create table t_max_case0022_cidr(c cidr);

--step2:text类型转换为inet; expect:192.168.1.0
insert into t_max_case0022_text values('192.168.0.1/24'),('192.168.0.0/25'),('192.168.1.0'),('192.168.1.0/25');
insert into t_max_case0022  select inet(t) from t_max_case0022_text;
select max(c) from  t_max_case0022;

--step3:clob类型转换为inet; expect:192.169.0.0/14
delete from t_max_case0022;
insert into t_max_case0022_clob values('192.168.255.1/14'),('192.169.0.0/14');
insert into t_max_case0022  select inet(c) from t_max_case0022_clob;
select max(c) from  t_max_case0022;

--step4:varchar类型转换为inet; expect:10.1.0.0/16
delete from t_max_case0022;
insert into t_max_case0022_varchar values('10.0.0.0/8'),('9.8.0.0/16'),('10.1.0.0/16');
insert into t_max_case0022  select inet(c) from t_max_case0022_varchar;
select max(c) from  t_max_case0022;

--step5:bpchar类型转换为inet; expect:192.168.100.128
delete from t_max_case0022;
insert into t_max_case0022_bpchar values('192.168.100.128/25'),('192.168.100.128');
insert into t_max_case0022  select inet(c) from t_max_case0022_bpchar;
select max(c) from  t_max_case0022;

--step6:nvarchar2类型转换为inet; expect:10.1.2.12
delete from t_max_case0022;
insert into t_max_case0022_nvarchar2 values('10.1.2.3/32'),('10.1.2.12'),('10.1.2.12/30');
insert into t_max_case0022  select inet(c) from t_max_case0022_nvarchar2;
select max(c) from  t_max_case0022;

--step7:cidr类型转换为inet; expect:10.1.2.12/31
delete from t_max_case0022;
insert into t_max_case0022_cidr values('10.1.2.3/32'),('10.1.2.12/31'),('10.1.2.12/30');
insert into t_max_case0022  select inet(c) from t_max_case0022_cidr;
select max(c) from  t_max_case0022;

--tearDown
drop table if exists t_max_case0022;
drop table if exists t_max_case0022_text;
drop table if exists t_max_case0022_clob;
drop table if exists t_max_case0022_varchar;
drop table if exists t_max_case0022_bpchar;
drop table if exists t_max_case0022_nvarchar2;
drop table if exists t_max_case0022_cidr;