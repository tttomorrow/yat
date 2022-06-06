-- @testpoint: inet类型取最小值，结果类型转换

--step1:创建表; expect:成功
drop table if exists t_min_case0019;
create table t_min_case0019(c inet);
create table t_min_case0019_text(t text);
create table t_min_case0019_clob(c clob);
create table t_min_case0019_varchar(c varchar);
create table t_min_case0019_bpchar(c bpchar);
create table t_min_case0019_nvarchar2(c nvarchar2);
create table t_min_case0019_cidr(c cidr);

--step2:输出转换为text; expect:192.168.0.1/24
insert into t_min_case0019 values('192.168.0.1/24'),('192.168.0.0/25'),('192.168.1.0'),('192.168.1.0/25');
insert into t_min_case0019_text select min(c) from  t_min_case0019;
select * from t_min_case0019_text;

--step3:输出转换为clob; expect:192.168.255.1/14
delete from t_min_case0019;
insert into t_min_case0019 values('192.168.255.1/14'),('192.169.0.0/14');
insert into t_min_case0019_clob select min(c) from  t_min_case0019;
select * from t_min_case0019_clob;

--step4:输出转换为varchar; expect:::
delete from t_min_case0019;
insert into t_min_case0019 values('::ffff'),('::'),('ff::ab/128');
insert into t_min_case0019_varchar select min(c) from  t_min_case0019;
select * from t_min_case0019_varchar;

--step5:输出转换为bpchar类型; expect:::
insert into t_min_case0019_bpchar select min(c) from  t_min_case0019;
select * from t_min_case0019_bpchar;

--step6:输出转换为nvarchar2; expect:::
insert into t_min_case0019_nvarchar2 select min(c) from  t_min_case0019;
select * from t_min_case0019_nvarchar2;

--step7:cidr类型转换为inet; expect:::/127
delete from t_min_case0019;
insert into t_min_case0019 values('::fff0/127'),('::/127'),('ff::ab/127');
insert into t_min_case0019_cidr select cidr(min(c)) from  t_min_case0019;
select * from t_min_case0019_cidr;

--tearDown
drop table if exists t_min_case0019;
drop table if exists t_min_case0019_text;
drop table if exists t_min_case0019_clob;
drop table if exists t_min_case0019_varchar;
drop table if exists t_min_case0019_bpchar;
drop table if exists t_min_case0019_nvarchar2;
drop table if exists t_min_case0019_cidr;