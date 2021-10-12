-- @testpoint: opengauss关键字subclass_origin非保留)，作为索引名,部分测试点合理报错

--前置条件，创建一个表
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists subclass_origin;
create index subclass_origin on explain_test(id);
drop index subclass_origin;

--关键字带双引号-成功
drop index if exists "subclass_origin";
create index "subclass_origin" on explain_test(id);
drop index "subclass_origin";

--关键字带单引号-合理报错
drop index if exists 'subclass_origin';
create index 'subclass_origin' on explain_test(id);

--关键字带反引号-合理报错
drop index if exists `subclass_origin`;
create index `subclass_origin` on explain_test(id);

--清理环境
drop table if exists explain_test;