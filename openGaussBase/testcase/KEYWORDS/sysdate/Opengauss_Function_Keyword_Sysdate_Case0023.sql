-- @testpoint: opengauss关键字sysdate(保留)，作为索引名,部分测试点合理报错

--前置条件，创建一个表
drop table if exists sysdate_test;
create table sysdate_test(id int,name varchar(10));

--关键字不带引号-失败
drop index if exists sysdate;
create index sysdate on sysdate_test(id);


--关键字带双引号-成功
drop index if exists "sysdate";
create index "sysdate" on sysdate_test(id);
drop index "sysdate";

--关键字带单引号-合理报错
drop index if exists 'sysdate';
create index 'sysdate' on sysdate_test(id);

--关键字带反引号-合理报错
drop index if exists `sysdate`;
create index `sysdate` on sysdate_test(id);

--清理环境
drop table if exists sysdate_test;