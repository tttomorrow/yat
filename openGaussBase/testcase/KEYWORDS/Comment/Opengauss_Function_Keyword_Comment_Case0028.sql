-- @testpoint: opengauss关键字comment(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists comment_test;
create table comment_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists comment;
create synonym comment for comment_test;
insert into comment values (1,'ada'),(2, 'bob');
update comment set comment.name='cici' where comment.id=2;
select * from comment;
drop synonym if exists comment;
--关键字带双引号-成功
drop synonym if exists "comment";
create synonym "comment" for comment_test;
drop synonym if exists "comment";

--关键字带单引号-合理报错
drop synonym if exists 'comment';
create synonym 'comment' for comment_test;
insert into 'comment' values (1,'ada'),(2, 'bob');
update 'comment' set 'comment'.name='cici' where 'comment'.id=2;
select * from 'comment';

--关键字带反引号-合理报错
drop synonym if exists `comment`;
create synonym `comment` for comment_test;
insert into `comment` values (1,'ada'),(2, 'bob');
update `comment` set `comment`.name='cici' where `comment`.id=2;
select * from `comment`;
drop table if exists comment_test;