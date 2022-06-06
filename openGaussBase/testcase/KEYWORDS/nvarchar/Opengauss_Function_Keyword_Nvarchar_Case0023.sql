-- @testpoint: opengauss关键字nvarchar非保留)，作为索引名,部分测试点合理报错

--step1:创建表;expect:成功
drop table if exists t_nvarchar_0023;
create table t_nvarchar_0023(id int,name varchar(10));

--step2:关键字不带引号;expect:成功
drop index if exists nvarchar;
create index nvarchar on t_nvarchar_0023(id);
drop index nvarchar;

--step3:关键字带双引号;expect:成功
drop index if exists "nvarchar";
create index "nvarchar" on t_nvarchar_0023(id);
drop index "nvarchar";

--step4:关键字带单引号;expect:合理报错
drop index if exists 'nvarchar';
create index 'nvarchar' on t_nvarchar_0023(id);

--step5:关键字带反引号;expect:合理报错
drop index if exists `nvarchar`;
create index `nvarchar` on t_nvarchar_0023(id);

--step6:清理环境;expect:成功
drop table if exists t_nvarchar_0023 cascade;
