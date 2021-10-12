-- @testpoint: opengauss关键字current_user(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists current_user_test;
create table current_user_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists current_user;
create synonym current_user for current_user_test;


--关键字带双引号-成功
drop synonym if exists "current_user";
create synonym "current_user" for current_user_test;
insert into "current_user" values (1,'ada'),(2, 'bob');
update "current_user" set "current_user".name='cici' where "current_user".id=2;
select * from "current_user";

--清理环境
drop synonym "current_user";

--关键字带单引号-合理报错
drop synonym if exists 'current_user';
create synonym 'current_user' for current_user_test;
insert into 'current_user' values (1,'ada'),(2, 'bob');
update 'current_user' set 'current_user'.name='cici' where 'current_user'.id=2;
select * from 'current_user';

--关键字带反引号-合理报错
drop synonym if exists `current_user`;
create synonym `current_user` for current_user_test;
insert into `current_user` values (1,'ada'),(2, 'bob');
update `current_user` set `current_user`.name='cici' where `current_user`.id=2;
select * from `current_user`;
drop table if exists current_user_test;