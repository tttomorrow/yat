-- @testpoint: opengauss关键字current(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists current_test;
create table current_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists current;
create synonym current for current_test;
insert into current values (1,'ada'),(2, 'bob');
update current set current.name='cici' where current.id=2;
select * from current;
drop synonym if exists current;
--关键字带双引号-成功
drop synonym if exists "current";
create synonym "current" for current_test;
drop synonym if exists "current";

--关键字带单引号-合理报错
drop synonym if exists 'current';
create synonym 'current' for current_test;
insert into 'current' values (1,'ada'),(2, 'bob');
update 'current' set 'current'.name='cici' where 'current'.id=2;
select * from 'current';

--关键字带反引号-合理报错
drop synonym if exists `current`;
create synonym `current` for current_test;
insert into `current` values (1,'ada'),(2, 'bob');
update `current` set `current`.name='cici' where `current`.id=2;
select * from `current`;
drop table if exists current_test;