-- @testpoint: min函数结合group by/having

--step1:创建表; expect:成功
drop table if exists t_min_case0014;
create table t_min_case0014(id int, i inet, c cidr);

--step2:max输入值为空 expect:空
select min(c) from  t_min_case0014;
select min(i) from  t_min_case0014;

--step3:max仅1个输入值 expect:0.0.1.1 ::
insert into t_min_case0014 values(1, '0.0.1.1', '::');
select min(i) from  t_min_case0014;
select min(c) from  t_min_case0014;

--step4:插入数据 expect:符合预期
insert into t_min_case0014 values(2, '2001:4f8:3:ba:2e0:81ff:254.34.209.241/128', '2001:4f8:3:ba:2e0:81ff:fe22:d1f2'),
(3, '2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128', '2001:4f8:3:ba:2e0:81ff:254.34.209.242');
insert into t_min_case0014 values(2, '2001:4f8:3:ba:2e0:81ff:254.34.209.240/128', '2001:4f8:3:ba:2e0:81ff:fe22:d1f0'),
(3, '2001:4f8:3:ba:2e0:81ff:fe22:d1f0/128', '2001:4f8:3:ba:2e0:81ff:254.34.209.240');
select id, min(i) from  t_min_case0014 group by id order by id;
select min(i) from  t_min_case0014;
select id, min(c) from  t_min_case0014 group by id order by id;
select min(c) from  t_min_case0014;

--step5:增加having; expect:符合预期
select id, min(i) from  t_min_case0014 group by id having count(id) <2 order by id;
select id, min(c) from  t_min_case0014 group by id having count(id) >1 order by id;

--tearDown
drop table if exists t_min_case0014;