-- @testpoint: opengauss关键字current_role(保留)，作为索引名，部分测试点合理报错

--前置条件，创建一个表
drop table if exists current_role_test;
create table current_role_test(id int,name varchar(10));

--关键字不带引号-合理报错
drop index if exists current_role;
create index current_role on current_role_test(id);


--关键字带双引号-成功
drop index if exists "current_role";
create index "current_role" on current_role_test(id);

--清理环境
drop index "current_role";

--关键字带单引号-合理报错
drop index if exists 'current_role';
create index 'current_role' on current_role_test(id);

--关键字带反引号-合理报错
drop index if exists `current_role`;
create index `current_role` on current_role_test(id);
drop table if exists current_role_test;