-- @testpoint: opengauss关键字session_user(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists session_user_test;
create table session_user_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists session_user;
create synonym session_user for session_user_test;


--关键字带双引号-成功
drop synonym if exists "session_user";
create synonym "session_user" for session_user_test;
insert into "session_user" values (1,'ada'),(2, 'bob');
update "session_user" set "session_user".name='cici' where "session_user".id=2;
select * from "session_user";

--清理环境
drop synonym "session_user";

--关键字带单引号-合理报错
drop synonym if exists 'session_user';
create synonym 'session_user' for session_user_test;
insert into 'session_user' values (1,'ada'),(2, 'bob');
update 'session_user' set 'session_user'.name='cici' where 'session_user'.id=2;
select * from 'session_user';

--关键字带反引号-合理报错
drop synonym if exists `session_user`;
create synonym `session_user` for session_user_test;
insert into `session_user` values (1,'ada'),(2, 'bob');
update `session_user` set `session_user`.name='cici' where `session_user`.id=2;
select * from `session_user`;
drop table if exists session_user_test;