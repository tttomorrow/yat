-- @testpoint: opengauss关键字following(非保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists following_test;
create table following_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists following;
create synonym following for following_test;
insert into following values (1,'ada'),(2, 'bob');
update following set following.name='cici' where following.id=2;
select * from following;
drop synonym if exists following;

--关键字带双引号-成功
drop synonym if exists "following";
create synonym "following" for following_test;
drop synonym if exists "following";

--关键字带单引号-合理报错
drop synonym if exists 'following';
create synonym 'following' for following_test;
insert into 'following' values (1,'ada'),(2, 'bob');
update 'following' set 'following'.name='cici' where 'following'.id=2;
select * from 'following';

--关键字带反引号-合理报错
drop synonym if exists `following`;
create synonym `following` for following_test;
insert into `following` values (1,'ada'),(2, 'bob');
update `following` set `following`.name='cici' where `following`.id=2;
select * from `following`;
drop table if exists following_test;