-- @testpoint: 非网络类型转换为cidr后ipv6地址取最大值

--step1:创建表; expect:成功
drop table if exists t_max_case0023;
create table t_max_case0023(c cidr);
create table t_max_case0023_text(t text);
create table t_max_case0023_clob(c clob);
create table t_max_case0023_varchar(c varchar);
create table t_max_case0023_bpchar(c bpchar);
create table t_max_case0023_nvarchar2(c nvarchar2);
create table t_max_case0023_inet(c inet);

--step2:text类型转换为cidr; expect:2001:4f8:3:ba::/65
insert into t_max_case0023_text values('2001:4f8:3:ba::/64'),('2001:4f8:3:ba::/65');
insert into t_max_case0023  select cidr(t) from t_max_case0023_text;
select max(c) from  t_max_case0023;

--step3:clob类型转换为cidr; expect:2001:4f8:3:ba:2e0:81ff:fe22:d1f2
delete from t_max_case0023;
insert into t_max_case0023_clob values('2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128'),('2001:4f8:3:ba:2e0:81ff:fe22:d1f2');
insert into t_max_case0023  select cidr(c) from t_max_case0023_clob;
select max(c) from  t_max_case0023;

--step4:varchar类型转换为cidr; expect:::ffff:1.2.3.0
delete from t_max_case0023;
insert into t_max_case0023_varchar values('::ffff:1.2.3.0/120'),('::ffff:1.2.3.0/128');
insert into t_max_case0023  select cidr(c) from t_max_case0023_varchar;
select max(c) from  t_max_case0023;

--step5:bpchar类型转换为cidr; expect:::ffff:2.2.3.0/120
delete from t_max_case0023;
insert into t_max_case0023_bpchar values('::ffff:2.2.3.0/120'),('::ffff:1.2.3.0/128');
insert into t_max_case0023  select cidr(c) from t_max_case0023_bpchar;
select max(c) from  t_max_case0023;

--step6:nvarchar2类型转换为cidr; expect:::ffff:1.2.3.0/120
delete from t_max_case0023;
insert into t_max_case0023_nvarchar2 values('::ffff:1.2.3.0/120'),('::ffff:12:30/128');
insert into t_max_case0023  select cidr(c) from t_max_case0023_nvarchar2;
select max(c) from  t_max_case0023;

--step7:inet类型转换为cidr; expect:::ffff:1.2.3.16/124
delete from t_max_case0023;
insert into t_max_case0023_inet values('::ffff:1.2.3.0/120'),('::ffff:0102:0310/124');
insert into t_max_case0023  select cidr(c) from t_max_case0023_inet;
select max(c) from  t_max_case0023;

--tearDown
drop table if exists t_max_case0023;
drop table if exists t_max_case0023_text;
drop table if exists t_max_case0023_clob;
drop table if exists t_max_case0023_varchar;
drop table if exists t_max_case0023_bpchar;
drop table if exists t_max_case0023_nvarchar2;
drop table if exists t_max_case0023_inet;