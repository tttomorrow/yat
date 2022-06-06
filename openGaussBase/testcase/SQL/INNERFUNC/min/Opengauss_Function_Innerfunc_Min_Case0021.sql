-- @testpoint: 1000w数据inet类型取最小值

--step1:创建表; expect:成功
drop table if exists t_min_case0021;
create table t_min_case0021(c inet);

--step2:批量插入数据; expect:成功
begin
for i in 1..1000000 LOOP
insert into t_min_case0021 values('255.255.255.255'), ('10.99.192.1/25'),('10.99.192.1/26'),('10.99.192.1/27');
end loop;
end;/

--step3:查询最小值; expect:10.99.192.1/25
select min(c) from t_min_case0021;

--step4:批量插入数据; expect:成功
begin
for i in 1..1000000 LOOP
insert into t_min_case0021 values('0.0.0.0'), ('10.99.192.1/25'),('10.99.192.1/25'),('10.99.192.1/25');
end loop;
end;/

--step5:查询最小值; expect:0.0.0.0
select min(c) from t_min_case0021;

--step6:批量插入数据; expect:成功
begin
for i in 1..500000 LOOP
insert into t_min_case0021 values('0.1.1.1'), ('::');
end loop;
end;/

--step7:查询最小值; expect:0.0.0.0
select min(c) from t_min_case0021;

--tearDown
drop table if exists t_min_case0021;