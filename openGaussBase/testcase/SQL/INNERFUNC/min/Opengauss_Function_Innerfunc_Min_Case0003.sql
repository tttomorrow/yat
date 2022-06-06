-- @testpoint: ipv4,ipv6混合取最小值

--step1:创建表; expect:成功
drop table if exists t_min_case0003;
create table t_min_case0003(id int, c cidr, i inet);

--step2:插入数据; expect:成功
insert into t_min_case0003 values(1,'192.168.100.128/25' ,'192.168.100.128/25'),
(2,'192.168.100.128/25' ,'192.168.100.128/24');
insert into t_min_case0003 values(3,'2001:4f8:3:ba:2e0:81ff:fe22:c000/116' ,'2001:4f8:3:ba:2e0:81ff:fe22:c000/116'),
(4,'2001:4f8:3:ba:2e0:81ff:254.34.192.0/116' ,'1.0.0.0'),(5,'1.0.0.0' ,'2001:4f8:3:ba:2e0:81ff:254.34.192.0/116');

--step3:查询最小值; expect:1.0.0.0
select min(c),min(i) from  t_min_case0003;

--tearDown
drop table if exists t_min_case0003;