-- @testpoint: max函数结合group by/having

--step1:创建表; expect:成功
drop table if exists t_max_case0025;
create table t_max_case0025(id int, i inet, c cidr);

--step2:max输入值为空 expect:空
select max(c) from  t_max_case0025;
select max(i) from  t_max_case0025;

--step3:max仅1个输入值 expect:0.0.1.1 ::
insert into t_max_case0025 values(1, '0.0.1.1', '::');
select max(i) from  t_max_case0025;
select max(c) from  t_max_case0025;

--step4:插入数据 expect:符合预期
insert into t_max_case0025 values(2, '2001:4f8:3:ba:2e0:81ff:254.34.209.241/128', '2001:4f8:3:ba:2e0:81ff:fe22:d1f2'),
(3, '2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128', '2001:4f8:3:ba:2e0:81ff:254.34.209.242');
insert into t_max_case0025 values(2, '2001:4f8:3:ba:2e0:81ff:254.34.209.240/128', '2001:4f8:3:ba:2e0:81ff:fe22:d1f0'),
(3, '2001:4f8:3:ba:2e0:81ff:fe22:d1f0/128', '2001:4f8:3:ba:2e0:81ff:254.34.209.240');
select id, max(i) from  t_max_case0025 group by id order by id;
select max(i) from  t_max_case0025;
select id, max(c) from  t_max_case0025 group by id order by id;
select max(c) from  t_max_case0025;

--step5:增加having; expect:符合预期
select id, max(i) from  t_max_case0025 group by id having count(id) <2 order by id;
select id, max(c) from  t_max_case0025 group by id having count(id) >1 order by id;

--tearDown
drop table if exists t_max_case0025;