-- @testpoint: opengauss关键字current_time(保留)，作为索引名，部分测试点合理报错

--前置条件，创建一个表
drop table if exists current_time_test;
create table current_time_test(id int,name varchar(10));

--关键字不带引号-合理报错
drop index if exists current_time;
create index current_time on current_time_test(id);


--关键字带双引号-成功
drop index if exists "current_time";
create index "current_time" on current_time_test(id);

--清理环境
drop index "current_time";

--关键字带单引号-合理报错
drop index if exists 'current_time';
create index 'current_time' on current_time_test(id);

--关键字带反引号-合理报错
drop index if exists `current_time`;
create index `current_time` on current_time_test(id);
drop table if exists current_time_test;