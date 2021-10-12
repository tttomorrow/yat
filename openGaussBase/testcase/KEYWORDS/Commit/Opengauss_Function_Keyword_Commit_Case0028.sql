-- @testpoint: opengauss关键字commit(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists commit_test;
create table commit_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists commit;
create synonym commit for commit_test;
insert into commit values (1,'ada'),(2, 'bob');
update commit set commit.name='cici' where commit.id=2;
select * from commit;
drop synonym if exists commit;
--关键字带双引号-成功
drop synonym if exists "commit";
create synonym "commit" for commit_test;
drop synonym if exists "commit";

--关键字带单引号-合理报错
drop synonym if exists 'commit';
create synonym 'commit' for commit_test;
insert into 'commit' values (1,'ada'),(2, 'bob');
update 'commit' set 'commit'.name='cici' where 'commit'.id=2;
select * from 'commit';

--关键字带反引号-合理报错
drop synonym if exists `commit`;
create synonym `commit` for commit_test;
insert into `commit` values (1,'ada'),(2, 'bob');
update `commit` set `commit`.name='cici' where `commit`.id=2;
select * from `commit`;
drop table if exists commit_test;