-- @testpoint: opengauss关键字remote(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists remote_test;
create table remote_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists remote;
create synonym remote for remote_test;
insert into remote values (1,'ada'),(2, 'bob');
update remote set remote.name='cici' where remote.id=2;
select * from remote;
drop synonym if exists remote;

--关键字带双引号-成功
drop synonym if exists "remote";
create synonym "remote" for remote_test;
insert into "remote" values (1,'ada'),(2, 'bob');
update "remote" set "remote".name='cici' where "remote".id=2;
select * from "remote";
drop synonym if exists "remote";

--关键字带单引号-合理报错
drop synonym if exists 'remote';

--关键字带反引号-合理报错
drop synonym if exists `remote`;
drop table if exists remote_test;