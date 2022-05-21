-- @testpoint: opengauss关键字nvarchar2(非保留)，作为字段数据类型(部分测试点合理报错)

--step1：关键字不带引号; expect: 执行成功
drop table if exists nvarchar2_test cascade;
create table nvarchar2_test(id int,name nvarchar2);

--step2：清理环境; expect: 执行成功
drop table if exists nvarchar2_test cascade;

--step3：关键字带双引号; expect: 执行成功
create table nvarchar2_test(id int,name "nvarchar2");

--step4：清理环境; expect: 执行成功
drop table if exists nvarchar2_test cascade;

--step5：关键字带单引号; expect: 合理报错
create table nvarchar2_test(id int,name 'nvarchar2');

--step6：关键字带反引号; expect: 合理报错
create table nvarchar2_test(id int,name `nvarchar2`);
