--  @testpoint:opengauss关键字group(保留)，作为索引名

--前置条件，创建一个表
drop table if exists group_test;
create table group_test(id int,name varchar(10));

--关键字不带引号-合理报错
drop index if exists group;
create index group on group_test(id);


--关键字带双引号-成功
drop index if exists "group";
create index "group" on group_test(id);

--清理环境
drop index "group";

--关键字带单引号-合理报错
drop index if exists 'group';
create index 'group' on group_test(id);

--关键字带反引号-合理报错
drop index if exists `group`;
create index `group` on group_test(id);