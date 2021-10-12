-- @testpoint: opengauss关键字user(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists user_test;
create table user_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists user;
create synonym user for user_test;

--关键字带双引号-成功
drop synonym if exists "user";
create synonym "user" for user_test;
insert into "user" values (1,'ada'),(2, 'bob');
update "user" set "user".name='cici' where "user".id=2;
select * from "user";
drop synonym "user";

--关键字带单引号-合理报错
drop synonym if exists 'user';
create synonym 'user' for user_test;
insert into 'user' values (1,'ada'),(2, 'bob');
update 'user' set 'user'.name='cici' where 'user'.id=2;
select * from 'user';

--关键字带反引号-合理报错
drop synonym if exists `user`;
create synonym `user` for user_test;
insert into `user` values (1,'ada'),(2, 'bob');
update `user` set `user`.name='cici' where `user`.id=2;
select * from `user`;
drop table if exists user_test;