-- @testpoint: opengauss关键字account(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists account_test;
create table account_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists account;
create synonym account for account_test;
insert into account values (1,'ada'),(2, 'bob');
update account set account.name='cici' where account.id=2;
select * from account;

--清理环境
drop synonym if exists account;

--关键字带双引号-成功
drop synonym if exists "account";
create synonym "account" for account_test;
insert into "account" values (1,'ada'),(2, 'bob');
update "account" set "account".name='cici' where "account".id=2;
select * from "account";

--清理环境
drop synonym if exists "account";

--关键字带单引号-合理报错
drop synonym if exists 'account';

--关键字带反引号-合理报错
drop synonym if exists `account`;
drop table if exists account_test;