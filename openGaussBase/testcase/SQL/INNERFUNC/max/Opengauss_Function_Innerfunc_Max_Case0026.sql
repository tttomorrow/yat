-- @testpoint: 函数中调用max

--step1:创建表; expect:成功
drop table if exists t_max_case0026_inet;
drop table if exists t_max_case0026_cidr;
create table t_max_case0026_inet(i inet);
create table t_max_case0026_cidr(c cidr);
insert into t_max_case0026_inet values('122.5.5.3/26'),('122.5.5.9/26');
insert into t_max_case0026_cidr values('122.5.5.3/32'),('122.5.5.9/32');

--step2:创建函数 expect:成功
create or replace function f_max_case0026_inet(out max_inet inet)
returns inet
as $$
begin
    select max(i) into max_inet from t_max_case0026_inet;
    return max_inet;
end;
$$language plpgsql;/

--step3:调用函数 expect:122.5.5.9/26
select f_max_case0026_inet();

--step4:调用函数 expect:122.5.5.3/32
insert into t_max_case0026_inet values('122.5.5.3/32');
select f_max_case0026_inet();

--step5:调用函数 expect:0.0.0.0
delete from t_max_case0026_inet;
insert into t_max_case0026_inet values('0.0.0.0');
select f_max_case0026_inet();

--step6:创建函数 expect:成功
create or replace function f_max_case0026_cidr(out max_cidr cidr)
returns cidr
as $$
begin
    select max(c) into max_cidr from t_max_case0026_cidr;
    raise info ':%',max_cidr;
    return max_cidr;
end;
$$language plpgsql;/

--step7:调用函数 expect:122.5.5.9/32
select f_max_case0026_cidr();

--step8:调用函数 expect:122.5.6.0/24
delete  from t_max_case0026_cidr;
insert into t_max_case0026_cidr values('122.5.6.0/24');
select f_max_case0026_cidr();

--step9:调用函数 expect:::
insert into t_max_case0026_cidr values('::');
select f_max_case0026_cidr();

--tearDown
drop function f_max_case0026_inet;
drop function f_max_case0026_cidr;
drop table if exists t_max_case0026_inet;
drop table if exists t_max_case0026_cidr;
