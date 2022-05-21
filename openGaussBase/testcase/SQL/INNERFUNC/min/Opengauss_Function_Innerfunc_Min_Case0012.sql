-- @testpoint: 非网络类型转换为cidr后ipv6地址取最小值

--step1:创建表; expect:成功
drop table if exists t_min_case0012;
create table t_min_case0012(c cidr);
create table t_min_case0012_text(t text);
create table t_min_case0012_clob(c clob);
create table t_min_case0012_varchar(c varchar);
create table t_min_case0012_bpchar(c bpchar);
create table t_min_case0012_nvarchar2(c nvarchar2);
create table t_min_case0012_inet(c inet);

--step2:text类型转换为cidr; expect:2001:4f8:3:ba::/64
insert into t_min_case0012_text values('2001:4f8:3:ba::/64'),('2001:4f8:3:ba::/65');
insert into t_min_case0012  select cidr(t) from t_min_case0012_text;
select min(c) from  t_min_case0012;

--step3:clob类型转换为cidr; expect:2001:4f8:3:ba:2e0:81ff:fe22:d1f1
delete from t_min_case0012;
insert into t_min_case0012_clob values('2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128'),('2001:4f8:3:ba:2e0:81ff:fe22:d1f2');
insert into t_min_case0012  select cidr(c) from t_min_case0012_clob;
select min(c) from  t_min_case0012;

--step4:varchar类型转换为cidr; expect:::ffff:1.2.3.0/120
delete from t_min_case0012;
insert into t_min_case0012_varchar values('::ffff:1.2.3.0/120'),('::ffff:1.2.3.0/128');
insert into t_min_case0012  select cidr(c) from t_min_case0012_varchar;
select min(c) from  t_min_case0012;

--step5:bpchar类型转换为cidr; expect:::ffff:1.2.3.0/128
delete from t_min_case0012;
insert into t_min_case0012_bpchar values('::ffff:2.2.3.0/120'),('::ffff:1.2.3.0/128');
insert into t_min_case0012  select cidr(c) from t_min_case0012_bpchar;
select min(c) from  t_min_case0012;

--step6:nvarchar2类型转换为cidr; expect:::ffff:0.18.0.48
delete from t_min_case0012;
insert into t_min_case0012_nvarchar2 values('::ffff:1.2.3.0/120'),('::ffff:12:30/128');
insert into t_min_case0012  select cidr(c) from t_min_case0012_nvarchar2;
select min(c) from  t_min_case0012;

--step7:inet类型转换为cidr; expect:::ffff:1.2.3.0/120
delete from t_min_case0012;
insert into t_min_case0012_inet values('::ffff:1.2.3.0/120'),('::ffff:0102:0310/124');
insert into t_min_case0012  select cidr(c) from t_min_case0012_inet;
select min(c) from  t_min_case0012;

--tearDown
drop table if exists t_min_case0012;
drop table if exists t_min_case0012_text;
drop table if exists t_min_case0012_clob;
drop table if exists t_min_case0012_varchar;
drop table if exists t_min_case0012_bpchar;
drop table if exists t_min_case0012_nvarchar2;
drop table if exists t_min_case0012_inet;