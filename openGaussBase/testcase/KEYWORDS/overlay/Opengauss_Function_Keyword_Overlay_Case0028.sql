-- @testpoint: opengauss关键字overlay(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists overlay;
create synonym overlay for explain_test;
insert into overlay values (1,'ada'),(2, 'bob');
update overlay set overlay.name='cici' where overlay.id=2;
select * from overlay;

--关键字带双引号-成功
drop synonym if exists "overlay";
create synonym "overlay" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'overlay';
create synonym 'overlay' for explain_test;
insert into 'overlay' values (1,'ada'),(2, 'bob');
update 'overlay' set 'overlay'.name='cici' where 'overlay'.id=2;
select * from 'overlay';

--关键字带反引号-合理报错
drop synonym if exists `overlay`;
create synonym `overlay` for explain_test;
insert into `overlay` values (1,'ada'),(2, 'bob');
update `overlay` set `overlay`.name='cici' where `overlay`.id=2;
select * from `overlay`;
--清理环境
drop synonym if exists "overlay";
drop synonym if exists overlay;
drop table if exists explain_test;