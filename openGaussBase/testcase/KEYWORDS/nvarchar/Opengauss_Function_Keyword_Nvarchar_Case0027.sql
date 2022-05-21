-- @testpoint: opengauss关键字nvarchar非保留，作为序列名 部分测试点合理报错


--step1:关键字不带引号;expect:成功
drop sequence if exists nvarchar;
create sequence nvarchar start 100 cache 50;
drop sequence nvarchar;

--step2:关键字带双引号;expect:成功
drop sequence if exists "nvarchar";
create sequence "nvarchar" start 100 cache 50;
drop sequence "nvarchar";

--step3:关键字带单引号;expect:合理报错
drop sequence if exists 'nvarchar';
create sequence 'nvarchar' start 100 cache 50;

--step4:关键字带反引号;expect:合理报错
drop sequence if exists `nvarchar`;
create sequence `nvarchar` start 100 cache 50;
