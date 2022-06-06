-- @testpoint: 函数中调用min

--step1:创建表; expect:成功
drop table if exists t_min_case0015_inet;
drop table if exists t_min_case0015_cidr;
create table t_min_case0015_inet(i inet);
create table t_min_case0015_cidr(c cidr);
insert into t_min_case0015_inet values('122.5.5.3/26'),('122.5.5.9/26');
insert into t_min_case0015_cidr values('122.5.5.3/32'),('122.5.5.9/32');

--step2:创建函数 expect:成功
create or replace function f_min_case0015_inet(out min_inet inet)
returns inet
as $$
begin
    select min(i) into min_inet from t_min_case0015_inet;
    return min_inet;
end;
$$language plpgsql;/

--step3:调用函数 expect:122.5.5.3/26
select f_min_case0015_inet();

--step4:调用函数 expect:122.5.5.3/32
delete from t_min_case0015_inet;
insert into t_min_case0015_inet values('122.5.5.3/32'),('::');
select f_min_case0015_inet();

--step5:调用函数 expect:0.0.0.0
delete from t_min_case0015_inet;
insert into t_min_case0015_inet values('0.0.0.0'),('::');
select f_min_case0015_inet();

--step6:创建函数 expect:成功
create or replace function f_min_case0015_cidr(out min_cidr cidr)
returns cidr
as $$
begin
    select min(c) into min_cidr from t_min_case0015_cidr;
    return min_cidr;
end;
$$language plpgsql;/

--step7:调用函数 expect:122.5.5.3/32
select f_min_case0015_cidr();

--step8:调用函数 expect:122.5.6.0/24
delete  from t_min_case0015_cidr;
insert into t_min_case0015_cidr values('122.5.6.0/24');
select f_min_case0015_cidr();

--step9:调用函数 expect:0.0.0.0
insert into t_min_case0015_cidr values('::'),('0.0.0.0');
select f_min_case0015_cidr();

--tearDown
drop function f_min_case0015_inet;
drop function f_min_case0015_cidr;
drop table if exists t_min_case0015_inet;
drop table if exists t_min_case0015_cidr;
