-- @testpoint: opengauss关键字system_user(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists system_user;
create synonym system_user for explain_test;
insert into system_user values (1,'ada'),(2, 'bob');
update system_user set system_user.name='cici' where system_user.id=2;
select * from system_user;
drop synonym if exists system_user;

--关键字带双引号-成功
drop synonym if exists "system_user";
create synonym "system_user" for explain_test;
drop synonym if exists "system_user";

--关键字带单引号-合理报错
drop synonym if exists 'system_user';
create synonym 'system_user' for explain_test;
insert into 'system_user' values (1,'ada'),(2, 'bob');
update 'system_user' set 'system_user'.name='cici' where 'system_user'.id=2;
select * from 'system_user';

--关键字带反引号-合理报错
drop synonym if exists `system_user`;
create synonym `system_user` for explain_test;
insert into `system_user` values (1,'ada'),(2, 'bob');
update `system_user` set `system_user`.name='cici' where `system_user`.id=2;
select * from `system_user`;

--清理环境
drop table if exists explain_test;