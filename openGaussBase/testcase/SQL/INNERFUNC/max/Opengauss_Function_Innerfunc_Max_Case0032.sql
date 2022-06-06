-- @testpoint: 1000w数据inet类型取最大值

--step1:创建表; expect:成功
drop table if exists t_max_case0032;
create table t_max_case0032(c inet);

--step2:批量插入数据; expect:成功
begin
for i in 1..1000000 LOOP
insert into t_max_case0032 values('0.0.0.0'), ('10.99.192.1/25'),('10.99.192.1/26'),('10.99.192.1/27');
end loop;
end;/

--step3:查询最大值; expect:10.99.192.1/27
select max(c) from t_max_case0032;

--step4:批量插入数据; expect:成功
begin
for i in 1..1000000 LOOP
insert into t_max_case0032 values('0.0.0.0'), ('10.99.192.1/25'),('10.99.192.1/25'),('10.99.192.1/25');
end loop;
end;/
insert into t_max_case0032 values ('10.99.192.1/32');

--step5:查询最大值; expect:10.99.192.1/32
select max(c) from t_max_case0032;

--step6:批量插入数据; expect:成功
begin
for i in 1..500000 LOOP
insert into t_max_case0032 values('10.255.255.255'), ('10.0.255.255');
end loop;
end;/

--step7:查询最大值; expect:10.255.255.255
select max(c) from t_max_case0032;

--tearDown
drop table if exists t_max_case0032;