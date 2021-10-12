-- @testpoint: opengauss关键字union(保留)，作为索引名,部分测试点合理报错

--前置条件，创建一个表
drop table if exists union_test;
create table union_test(id int,name varchar(10));

--关键字不带引号-失败
drop index if exists union;
create index union on union_test(id);


--关键字带双引号-成功
drop index if exists "union";
create index "union" on union_test(id);
drop index "union";

--关键字带单引号-合理报错
drop index if exists 'union';
create index 'union' on union_test(id);

--关键字带反引号-合理报错
drop index if exists `union`;
create index `union` on union_test(id);

--清理环境
drop table if exists union_test;