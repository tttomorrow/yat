-- @testpoint: opengauss关键字dispatch(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists dispatch_test;
create table dispatch_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists dispatch;
create synonym dispatch for dispatch_test;
insert into dispatch values (1,'ada'),(2, 'bob');
update dispatch set dispatch.name='cici' where dispatch.id=2;
select * from dispatch;
drop synonym if exists dispatch;

--关键字带双引号-成功
drop synonym if exists "dispatch";
create synonym "dispatch" for dispatch_test;
drop synonym if exists "dispatch";

--关键字带单引号-合理报错
drop synonym if exists 'dispatch';
create synonym 'dispatch' for dispatch_test;
insert into 'dispatch' values (1,'ada'),(2, 'bob');
update 'dispatch' set 'dispatch'.name='cici' where 'dispatch'.id=2;
select * from 'dispatch';

--关键字带反引号-合理报错
drop synonym if exists `dispatch`;
create synonym `dispatch` for dispatch_test;
insert into `dispatch` values (1,'ada'),(2, 'bob');
update `dispatch` set `dispatch`.name='cici' where `dispatch`.id=2;
select * from `dispatch`;
drop table if exists dispatch_test;