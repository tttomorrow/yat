-- @testpoint: opengauss关键字existing(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists existing_test;
create table existing_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists existing;
create synonym existing for existing_test;
insert into existing values (1,'ada'),(2, 'bob');
update existing set existing.name='cici' where existing.id=2;
select * from existing;
drop synonym if exists existing;

--关键字带双引号-成功
drop synonym if exists "existing";
create synonym "existing" for existing_test;
drop synonym if exists "existing";

--关键字带单引号-合理报错
drop synonym if exists 'existing';
create synonym 'existing' for existing_test;
insert into 'existing' values (1,'ada'),(2, 'bob');
update 'existing' set 'existing'.name='cici' where 'existing'.id=2;
select * from 'existing';

--关键字带反引号-合理报错
drop synonym if exists `existing`;
create synonym `existing` for existing_test;
insert into `existing` values (1,'ada'),(2, 'bob');
update `existing` set `existing`.name='cici' where `existing`.id=2;
select * from `existing`;
drop table if exists existing_test;