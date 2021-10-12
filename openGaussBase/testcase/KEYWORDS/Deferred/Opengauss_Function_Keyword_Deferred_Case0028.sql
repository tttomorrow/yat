-- @testpoint: opengauss关键字deferred(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists deferred_test;
create table deferred_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists deferred;
create synonym deferred for deferred_test;
insert into deferred values (1,'ada'),(2, 'bob');
update deferred set deferred.name='cici' where deferred.id=2;
select * from deferred;
drop synonym if exists deferred;

--关键字带双引号-成功
drop synonym if exists "deferred";
create synonym "deferred" for deferred_test;
drop synonym if exists "deferred";

--关键字带单引号-合理报错
drop synonym if exists 'deferred';
create synonym 'deferred' for deferred_test;
insert into 'deferred' values (1,'ada'),(2, 'bob');
update 'deferred' set 'deferred'.name='cici' where 'deferred'.id=2;
select * from 'deferred';

--关键字带反引号-合理报错
drop synonym if exists `deferred`;
create synonym `deferred` for deferred_test;
insert into `deferred` values (1,'ada'),(2, 'bob');
update `deferred` set `deferred`.name='cici' where `deferred`.id=2;
select * from `deferred`;
drop table if exists deferred_test;