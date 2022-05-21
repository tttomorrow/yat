-- @testpoint: 非网络类型转换为inet后ipv6地址取最大值

--step1:创建表; expect:成功
drop table if exists t_max_case0024;
create table t_max_case0024(c inet);
create table t_max_case0024_text(t text);
create table t_max_case0024_clob(c clob);
create table t_max_case0024_varchar(c varchar);
create table t_max_case0024_bpchar(c bpchar);
create table t_max_case0024_nvarchar2(c nvarchar2);
create table t_max_case0024_cidr(c cidr);

--step2:text类型转换为inet; expect:2001:4f8:3:ba::/65
insert into t_max_case0024_text values('2001:4f8:3:ba::/64'),('2001:4f8:3:ba::/65');
insert into t_max_case0024  select inet(t) from t_max_case0024_text;
select max(c) from  t_max_case0024;

--step3:clob类型转换为inet; expect:2001:4f8:3:ba:2e0:81ff:fe22:d1f2
delete from t_max_case0024;
insert into t_max_case0024_clob values('2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128'),('2001:4f8:3:ba:2e0:81ff:fe22:d1f2');
insert into t_max_case0024  select inet(c) from t_max_case0024_clob;
select max(c) from  t_max_case0024;

--step4:varchar类型转换为inet; expect:::ffff:1.2.3.0
delete from t_max_case0024;
insert into t_max_case0024_varchar values('::ffff:1.2.3.0/120'),('::ffff:1.2.3.0/128');
insert into t_max_case0024  select inet(c) from t_max_case0024_varchar;
select max(c) from  t_max_case0024;

--step5:bpchar类型转换为inet; expect:::ffff:2.2.3.0/120
delete from t_max_case0024;
insert into t_max_case0024_bpchar values('::ffff:2.2.3.0/120'),('::ffff:1.2.3.0/128');
insert into t_max_case0024  select inet(c) from t_max_case0024_bpchar;
select max(c) from  t_max_case0024;

--step6:nvarchar2类型转换为inet; expect:::ffff:1.2.3.0/120
delete from t_max_case0024;
insert into t_max_case0024_nvarchar2 values('::ffff:1.2.3.0/120'),('::ffff:12:30/128');
insert into t_max_case0024  select inet(c) from t_max_case0024_nvarchar2;
select max(c) from  t_max_case0024;

--step7:cidr类型转换为inet; expect:::ffff:1.2.3.16/124
delete from t_max_case0024;
insert into t_max_case0024_cidr values('::ffff:1.2.3.0/120'),('::ffff:0102:0310/124');
insert into t_max_case0024  select inet(c) from t_max_case0024_cidr;
select max(c) from  t_max_case0024;

--tearDown
drop table if exists t_max_case0024;
drop table if exists t_max_case0024_text;
drop table if exists t_max_case0024_clob;
drop table if exists t_max_case0024_varchar;
drop table if exists t_max_case0024_bpchar;
drop table if exists t_max_case0024_nvarchar2;
drop table if exists t_max_case0024_cidr;