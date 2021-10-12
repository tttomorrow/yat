--  @testpoint:opengauss关键字cube(非保留)，作为字段数据类型(合理报错)

--前置条件
drop table if exists cube_test cascade;

--关键字不带引号-合理报错
create table cube_test(id int,name cube);
---目前测试结果，拿数据库的非初始用户登录，创建成功了，cube是什么数据类型，待确认

--关键字带双引号-合理报错
drop table if exists cube_test cascade;
create table cube_test(id int,name "cube");
---目前测试结果，拿数据库的非初始用户登录，创建成功了，cube是什么数据类型，待确认

--关键字带单引号-合理报错
drop table if exists cube_test cascade;
create table cube_test(id int,name 'cube');

--关键字带反引号-合理报错
create table cube_test(id int,name `cube`);
