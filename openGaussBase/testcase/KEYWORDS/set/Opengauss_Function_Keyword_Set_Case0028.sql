-- @testpoint: opengauss关键字set(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists set;
create synonym set for explain_test;
insert into set values (1,'ada'),(2, 'bob');
update set set set.name='cici' where set.id=2;
select * from set;
drop synonym if exists set;

--关键字带双引号-成功
drop synonym if exists "set";
create synonym "set" for explain_test;
drop synonym if exists "set";

--关键字带单引号-合理报错
drop synonym if exists 'set';
create synonym 'set' for explain_test;
insert into 'set' values (1,'ada'),(2, 'bob');
update 'set' set 'set'.name='cici' where 'set'.id=2;
select * from 'set';

--关键字带反引号-合理报错
drop synonym if exists `set`;
create synonym `set` for explain_test;
insert into `set` values (1,'ada'),(2, 'bob');
update `set` set `set`.name='cici' where `set`.id=2;
select * from `set`;
drop table if exists explain_test;