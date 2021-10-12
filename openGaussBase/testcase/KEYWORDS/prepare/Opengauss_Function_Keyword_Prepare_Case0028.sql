-- @testpoint: opengauss关键字prepare(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists prepare_test;
create table prepare_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists prepare;
create synonym prepare for prepare_test;
insert into prepare values (1,'ada'),(2, 'bob');
update prepare set prepare.name='cici' where prepare.id=2;
select * from prepare;

--关键字带双引号-成功
drop synonym if exists "prepare";
create synonym "prepare" for prepare_test;
insert into "prepare" values (1,'ada'),(2, 'bob');
update "prepare" set "prepare".name='cici' where "prepare".id=2;
select * from "prepare";

--关键字带单引号-合理报错
drop synonym if exists 'prepare';
create synonym 'prepare' for prepare_test;

--关键字带反引号-合理报错
drop synonym if exists `prepare`;
create synonym `prepare` for prepare_test;
--清理环境
drop synonym if exists "prepare";
drop synonym if exists prepare;
drop table if exists prepare_test;
