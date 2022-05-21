-- @testpoint: 非网络类型转换为cidr后ipv4地址取最小值

--step1:创建表; expect:成功
drop table if exists t_min_case0010;
create table t_min_case0010(c cidr);
create table t_min_case0010_text(t text);
create table t_min_case0010_clob(c clob);
create table t_min_case0010_varchar(c varchar);
create table t_min_case0010_bpchar(c bpchar);
create table t_min_case0010_nvarchar2(c nvarchar2);
create table t_min_case0010_inet(c inet);

--step2:text类型转换为cidr; expect:192.168.0.0/24
insert into t_min_case0010_text values('192.168/24'),('192.168/25'),('192.168.1'),('192.168');
insert into t_min_case0010  select cidr(t) from t_min_case0010_text;
select min(c) from  t_min_case0010;

--step3:clob类型转换为cidr; expect:192.168.0.0/14
delete from t_min_case0010;
insert into t_min_case0010_clob values('192.168'),('192.168/14');
insert into t_min_case0010  select cidr(c) from t_min_case0010_clob;
select min(c) from  t_min_case0010;

--step4:varchar类型转换为cidr; expect:9.8.0.0/16
delete from t_min_case0010;
insert into t_min_case0010_varchar values('10'),('9.8'),('10.1');
insert into t_min_case0010  select cidr(c) from t_min_case0010_varchar;
select min(c) from  t_min_case0010;

--step5:bpchar类型转换为cidr; expect:192.168.100.128/25
delete from t_min_case0010;
insert into t_min_case0010_bpchar values('192.168.100.128/25'),('192.168.100.128');
insert into t_min_case0010  select cidr(c) from t_min_case0010_bpchar;
select min(c) from  t_min_case0010;

--step6:nvarchar2类型转换为cidr; expect:10.1.2.3/32
delete from t_min_case0010;
insert into t_min_case0010_nvarchar2 values('10.1.2.3/32'),('10.1.2.12'),('10.1.2.12/30');
insert into t_min_case0010  select cidr(c) from t_min_case0010_nvarchar2;
select min(c) from  t_min_case0010;

--step7:inet类型转换为cidr; expect:10.1.2.2/31
delete from t_min_case0010;
insert into t_min_case0010_inet values('10.1.2.3/31'),('10.1.2.12/31'),('10.1.2.12/30');
insert into t_min_case0010  select cidr(c) from t_min_case0010_inet;
select min(c) from  t_min_case0010;

--tearDown
drop table if exists t_min_case0010;
drop table if exists t_min_case0010_text;
drop table if exists t_min_case0010_clob;
drop table if exists t_min_case0010_varchar;
drop table if exists t_min_case0010_bpchar;
drop table if exists t_min_case0010_nvarchar2;
drop table if exists t_min_case0010_inet;