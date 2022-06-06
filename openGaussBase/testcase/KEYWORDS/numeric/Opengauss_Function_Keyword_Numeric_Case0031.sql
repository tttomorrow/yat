-- @testpoint: opengauss关键字numeric(非保留)，作为字段数据类型(部分测试点合理报错)

--step1：关键字不带引号; expect: 执行成功
drop table if exists numeric_test cascade;
create table numeric_test(id int,name numeric);

--step2：清理环境; expect: 执行成功
drop table if exists numeric_test cascade;

--step3：关键字带双引号; expect: 执行成功
create table numeric_test(id int,name "numeric");

--step4：清理环境; expect: 执行成功
drop table if exists numeric_test cascade;

--step5：关键字带单引号; expect: 合理报错
create table numeric_test(id int,name 'numeric');

--step6：关键字带反引号; expect: 合理报错
create table numeric_test(id int,name `numeric`);
