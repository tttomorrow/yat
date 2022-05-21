-- @testpoint: opengauss关键字text(非保留)，作为字段数据类型(部分测试点合理报错)

--step1：关键字不带引号; expect: 执行成功
drop table if exists text_test cascade;
create table text_test(id int,name text);

--step2：清理环境; expect: 执行成功
drop table if exists text_test cascade;

--step3：关键字带双引号; expect: 执行成功
create table text_test(id int,name "text");

--step4：清理环境; expect: 执行成功
drop table if exists text_test cascade;

--step5：关键字带单引号; expect: 合理报错
create table text_test(id int,name 'text');

--step6：关键字带反引号; expect: 合理报错
create table text_test(id int,name `text`);
