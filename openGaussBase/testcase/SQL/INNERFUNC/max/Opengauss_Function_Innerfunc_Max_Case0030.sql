-- @testpoint: inet类型取最大值，结果类型转换

--step1:创建表; expect:成功
drop table if exists t_max_case0030;
create table t_max_case0030(c inet);
create table t_max_case0030_text(t text);
create table t_max_case0030_clob(c clob);
create table t_max_case0030_varchar(c varchar);
create table t_max_case0030_bpchar(c bpchar);
create table t_max_case0030_nvarchar2(c nvarchar2);
create table t_max_case0030_cidr(c cidr);

--step2:输出转换为text; expect:192.168.1.0
insert into t_max_case0030 values('192.168.0.1/24'),('192.168.0.0/25'),('192.168.1.0'),('192.168.1.0/25');
insert into t_max_case0030_text select max(c) from  t_max_case0030;
select * from t_max_case0030_text;

--step3:输出转换为clob; expect:192.169.0.0/14
delete from t_max_case0030;
insert into t_max_case0030 values('192.168.255.1/14'),('192.169.0.0/14');
insert into t_max_case0030_clob select max(c) from  t_max_case0030;
select * from t_max_case0030_clob;

--step4:输出转换为varchar; expect:ff::ab
delete from t_max_case0030;
insert into t_max_case0030 values('::ffff'),('::'),('ff::ab/128');
insert into t_max_case0030_varchar select max(c) from  t_max_case0030;
select * from t_max_case0030_varchar;

--step5:输出转换为bpchar类型; expect:ff::ab
insert into t_max_case0030_bpchar select max(c) from  t_max_case0030;
select * from t_max_case0030_bpchar;

--step6:输出转换为nvarchar2; expect:ff::ab
insert into t_max_case0030_nvarchar2 select max(c) from  t_max_case0030;
select * from t_max_case0030_nvarchar2;

--step7:cidr类型转换为inet; expect:ff::aa/127
delete from t_max_case0030;
insert into t_max_case0030 values('::fff0/127'),('::/127'),('ff::ab/127');
insert into t_max_case0030_cidr select cidr(max(c)) from  t_max_case0030;
select * from t_max_case0030_cidr;

--tearDown
drop table if exists t_max_case0030;
drop table if exists t_max_case0030_text;
drop table if exists t_max_case0030_clob;
drop table if exists t_max_case0030_varchar;
drop table if exists t_max_case0030_bpchar;
drop table if exists t_max_case0030_nvarchar2;
drop table if exists t_max_case0030_cidr;