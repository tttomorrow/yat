-- @testpoint: opengauss关键字reindex非保留)，作为索引名，部分测试点合理报错

--前置条件，创建一个表
drop table if exists reindex_test;
create table reindex_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists reindex;
create index reindex on reindex_test(id);
drop index reindex;

--关键字带双引号-成功
drop index if exists "reindex";
create index "reindex" on reindex_test(id);
drop index "reindex";

--关键字带单引号-合理报错
drop index if exists 'reindex';


--关键字带反引号-合理报错
drop index if exists `reindex`;
drop table if exists reindex_test;
