-- @testpoint: opengauss关键字user(保留)，作为索引名，部分测试点合理报错

--前置条件，创建一个表
drop table if exists user_test;
create table user_test(id int,name varchar(10));

--关键字不带引号-失败
drop index if exists user;
create index user on user_test(id);


--关键字带双引号-成功
drop index if exists "user";
create index "user" on user_test(id);
drop index "user";

--关键字带单引号-合理报错
drop index if exists 'user';
create index 'user' on user_test(id);

--关键字带反引号-合理报错
drop index if exists `user`;
create index `user` on user_test(id);
drop table if exists user_test;