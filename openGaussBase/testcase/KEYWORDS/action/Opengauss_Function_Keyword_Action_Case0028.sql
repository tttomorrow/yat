-- @testpoint: opengauss关键字action(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists action_test;
create table action_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists action;
create synonym action for action_test;
insert into action values (1,'ada'),(2, 'bob');
update action set action.name='cici' where action.id=2;
select * from action;

--清理环境
drop synonym if exists action;

--关键字带双引号-成功
drop synonym if exists "action";
create synonym "action" for action_test;
insert into "action" values (1,'ada'),(2, 'bob');
update "action" set "action".name='cici' where "action".id=2;
select * from "action";

--清理环境
drop synonym if exists "action";
drop table if exists action_test;

--关键字带单引号-合理报错
drop synonym if exists 'action';

--关键字带反引号-合理报错
drop synonym if exists `action`;
