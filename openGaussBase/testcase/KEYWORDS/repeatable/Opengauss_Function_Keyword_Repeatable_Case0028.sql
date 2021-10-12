-- @testpoint: opengauss关键字repeatable(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists repeatable_test;
create table repeatable_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists repeatable;
create synonym repeatable for repeatable_test;
insert into repeatable values (1,'ada'),(2, 'bob');
update repeatable set repeatable.name='cici' where repeatable.id=2;
select * from repeatable;
drop synonym if exists repeatable;

--关键字带双引号-成功
drop synonym if exists "repeatable";
create synonym "repeatable" for repeatable_test;
insert into "repeatable" values (1,'ada'),(2, 'bob');
update "repeatable" set "repeatable".name='cici' where "repeatable".id=2;
select * from "repeatable";
drop synonym if exists "repeatable";

--关键字带单引号-合理报错
drop synonym if exists 'repeatable';

--关键字带反引号-合理报错
drop synonym if exists `repeatable`;
drop table if exists repeatable_test;