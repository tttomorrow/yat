-- @testpoint: opengauss关键字cursor_name(非保留)，作为索引名，部分测试点合理报错

--前置条件，创建一个表
drop table if exists cursor_name_test;
create table cursor_name_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists cursor_name;
create index cursor_name on cursor_name_test(id);
drop index cursor_name;

--关键字带双引号-成功
drop index if exists "cursor_name";
create index "cursor_name" on cursor_name_test(id);
drop index "cursor_name";

--关键字带单引号-合理报错
drop index if exists 'cursor_name';
create index 'cursor_name' on cursor_name_test(id);

--关键字带反引号-合理报错
drop index if exists `cursor_name`;
create index `cursor_name` on cursor_name_test(id);
drop table if exists cursor_name_test;