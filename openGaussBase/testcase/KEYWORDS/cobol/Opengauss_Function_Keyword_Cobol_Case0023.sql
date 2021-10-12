-- @testpoint: opengauss关键字cobol非保留)，作为索引名，部分测试点合理报错
--前置条件，创建一个表
drop table if exists cobol_test;
create table cobol_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists cobol;
create index cobol on cobol_test(id);

--清理环境
drop index cobol;

--关键字带双引号-成功
drop index if exists "cobol";
create index "cobol" on cobol_test(id);

--清理环境
drop index "cobol";

--关键字带单引号-合理报错
drop index if exists 'cobol';

--关键字带反引号-合理报错
drop index if exists `cobol`;
drop table if exists cobol_test;