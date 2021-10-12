-- @testpoint: opengauss关键字within(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists within;
create synonym within for explain_test;
insert into within values (1,'ada'),(2, 'bob');
update within set within.name='cici' where within.id=2;
select * from within;
drop synonym if exists within;

--关键字带双引号-成功
drop synonym if exists "within";
create synonym "within" for explain_test;
drop synonym if exists "within";

--关键字带单引号-合理报错
drop synonym if exists 'within';
create synonym 'within' for explain_test;
insert into 'within' values (1,'ada'),(2, 'bob');
update 'within' set 'within'.name='cici' where 'within'.id=2;
select * from 'within';

--关键字带反引号-合理报错
drop synonym if exists `within`;
create synonym `within` for explain_test;
insert into `within` values (1,'ada'),(2, 'bob');
update `within` set `within`.name='cici' where `within`.id=2;
select * from `within`;
drop table if exists explain_test;