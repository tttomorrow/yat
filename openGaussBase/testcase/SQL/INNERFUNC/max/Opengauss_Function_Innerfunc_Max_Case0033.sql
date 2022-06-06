-- @testpoint: 1000w数据cidr类型取最大值

--step1:创建表; expect:成功
drop table if exists t_max_case0033;
create table t_max_case0033(c cidr);

--step2:批量插入数据; expect:成功
begin
for i in 1..1000000 LOOP
insert into t_max_case0033 values('122.5.5.3/32'), ('122.5.5.9/32'),('122.95.5.0/30'),('122.95.5.0/31');
end loop;
end;/

--step3:查询最大值; expect:122.95.5.0/31
select max(c) from t_max_case0033;

--step4:批量插入数据; expect:成功
begin
for i in 1..1000000 LOOP
insert into t_max_case0033 values('122.5.5.3/32'), ('122.5.5.9/32'),('122.95.5.0/30'),('::');
end loop;
end;/

--step5:查询最大值; expect:::
select max(c) from t_max_case0033;

--step6:批量插入数据; expect:成功
begin
for i in 1..500000 LOOP
insert into t_max_case0033 values('::ffff'), ('::0:0:0:0:0.0.0.0');
end loop;
end;/

--step7:查询最大值; expect:::ffff
select max(c) from t_max_case0033;

--tearDown
drop table if exists t_max_case0033;