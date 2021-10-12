-- @testpoint: opengauss关键字after(非保留)，作为索引名，部分测试点合理报错
--前置条件，创建一个表
drop table if exists after_test;
create table after_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists after;
create index after on after_test(id);

--清理环境
drop index after;

--关键字带双引号-成功
drop index if exists "after";
create index "after" on after_test(id);

--清理环境
drop index "after";

--关键字带单引号-合理报错
drop index if exists 'after';

--关键字带反引号-合理报错
drop index if exists `after`;
drop table if exists after_test;