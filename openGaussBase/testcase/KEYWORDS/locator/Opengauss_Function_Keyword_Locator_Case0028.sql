-- @testpoint: opengauss关键字locator(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists locator;
create synonym locator for explain_test;
insert into locator values (1,'ada'),(2, 'bob');
update locator set locator.name='cici' where locator.id=2;
select * from locator;

--关键字带双引号-成功
drop synonym if exists "locator";
create synonym "locator" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'locator';
create synonym 'locator' for explain_test;
insert into 'locator' values (1,'ada'),(2, 'bob');
update 'locator' set 'locator'.name='cici' where 'locator'.id=2;
select * from 'locator';

--关键字带反引号-合理报错
drop synonym if exists `locator`;
create synonym `locator` for explain_test;
insert into `locator` values (1,'ada'),(2, 'bob');
update `locator` set `locator`.name='cici' where `locator`.id=2;
select * from `locator`;
--清理环境
drop synonym if exists locator;
drop table if exists explain_test;