-- @testpoint: opengauss关键字desc(保留)，作为索引名，部分测试点合理报错

--前置条件，创建一个表
drop table if exists desc_test;
create table desc_test(id int,name varchar(10));

--关键字不带引号-失败
drop index if exists desc;
create index desc on desc_test(id);


--关键字带双引号-成功
drop index if exists "desc";
create index "desc" on desc_test(id);
drop index "desc";

--关键字带单引号-合理报错
drop index if exists 'desc';
create index 'desc' on desc_test(id);

--关键字带反引号-合理报错
drop index if exists `desc`;
create index `desc` on desc_test(id);
drop table if exists desc_test;