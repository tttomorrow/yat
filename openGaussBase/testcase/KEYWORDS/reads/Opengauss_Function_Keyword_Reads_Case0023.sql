-- @testpoint: opengauss关键字reads非保留)，作为索引名,部分测试点合理报错

--前置条件，创建一个表
drop table if exists reads_test;
create table reads_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists reads;
create index reads on reads_test(id);
drop index reads;

--关键字带双引号-成功
drop index if exists "reads";
create index "reads" on reads_test(id);
drop index "reads";

--关键字带单引号-合理报错
drop index if exists 'reads';


--关键字带反引号-合理报错
drop index if exists `reads`;
--清理环境
drop table if exists reads_test;
