-- @testpoint: opengauss关键字replica非保留)，作为索引名，部分测试点合理报错

--前置条件，创建一个表
drop table if exists replica_test;
create table replica_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists replica;
create index replica on replica_test(id);
drop index replica;

--关键字带双引号-成功
drop index if exists "replica";
create index "replica" on replica_test(id);
drop index "replica";

--关键字带单引号-合理报错
drop index if exists 'replica';


--关键字带反引号-合理报错
drop index if exists `replica`;
drop table if exists replica_test;
