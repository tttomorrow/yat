-- @testpoint: 非网络类型转换为cidr后ipv4地址取最大值

--step1:创建表; expect:成功
drop table if exists t_max_case0021;
create table t_max_case0021(c cidr);
create table t_max_case0021_text(t text);
create table t_max_case0021_clob(c clob);
create table t_max_case0021_varchar(c varchar);
create table t_max_case0021_bpchar(c bpchar);
create table t_max_case0021_nvarchar2(c nvarchar2);
create table t_max_case0021_inet(c inet);

--step2:text类型转换为cidr; expect:192.168.1.0/24
insert into t_max_case0021_text values('192.168/24'),('192.168/25'),('192.168.1'),('192.168');
insert into t_max_case0021  select cidr(t) from t_max_case0021_text;
select max(c) from  t_max_case0021;

--step3:clob类型转换为cidr; expect:192.168.0.0/24
delete from t_max_case0021;
insert into t_max_case0021_clob values('192.168'),('192.168/14');
insert into t_max_case0021  select cidr(c) from t_max_case0021_clob;
select max(c) from  t_max_case0021;

--step4:varchar类型转换为cidr; expect:10.1.0.0/16
delete from t_max_case0021;
insert into t_max_case0021_varchar values('10'),('9.8'),('10.1');
insert into t_max_case0021  select cidr(c) from t_max_case0021_varchar;
select max(c) from  t_max_case0021;

--step5:bpchar类型转换为cidr; expect:192.168.100.128/32
delete from t_max_case0021;
insert into t_max_case0021_bpchar values('192.168.100.128/25'),('192.168.100.128');
insert into t_max_case0021  select cidr(c) from t_max_case0021_bpchar;
select max(c) from  t_max_case0021;

--step6:nvarchar2类型转换为cidr; expect:10.1.2.12
delete from t_max_case0021;
insert into t_max_case0021_nvarchar2 values('10.1.2.3/32'),('10.1.2.12'),('10.1.2.12/30');
insert into t_max_case0021  select cidr(c) from t_max_case0021_nvarchar2;
select max(c) from  t_max_case0021;

--step7:inet类型转换为cidr; expect:10.1.2.12/31
delete from t_max_case0021;
insert into t_max_case0021_inet values('10.1.2.3/31'),('10.1.2.12/31'),('10.1.2.12/30');
insert into t_max_case0021  select cidr(c) from t_max_case0021_inet;
select max(c) from  t_max_case0021;

--tearDown
drop table if exists t_max_case0021;
drop table if exists t_max_case0021_text;
drop table if exists t_max_case0021_clob;
drop table if exists t_max_case0021_varchar;
drop table if exists t_max_case0021_bpchar;
drop table if exists t_max_case0021_nvarchar2;
drop table if exists t_max_case0021_inet;