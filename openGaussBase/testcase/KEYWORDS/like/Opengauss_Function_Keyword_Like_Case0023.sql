-- @testpoint: opengauss关键字like(保留)，作为索引名 合理报错

--前置条件，创建一个表
drop table if exists like_test;
create table like_test(id int,name varchar(10));

--关键字不带引号-合理报错
drop index if exists like;
create index like on like_test(id);


--关键字带双引号-成功
drop index if exists "like";
create index "like" on like_test(id);

--清理环境
drop index "like";

--关键字带单引号-合理报错
drop index if exists 'like';
create index 'like' on like_test(id);

--关键字带反引号-合理报错
drop index if exists `like`;
create index `like` on like_test(id);
--清理环境
drop table if exists like_test cascade;