-- @testpoint: opengauss关键字begin(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists begin_test;
create table begin_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists begin;
create synonym begin for begin_test;
insert into begin values (1,'ada'),(2, 'bob');
update begin set begin.name='cici' where begin.id=2;
select * from begin;

--清理环境
drop synonym if exists begin;

--关键字带双引号-成功
drop synonym if exists "begin";
create synonym "begin" for begin_test;
insert into "begin" values (1,'ada'),(2, 'bob');
update "begin" set "begin".name='cici' where "begin".id=2;
select * from "begin";

--清理环境
drop synonym if exists "begin";

--关键字带单引号-合理报错
drop synonym if exists 'begin';

--关键字带反引号-合理报错
drop synonym if exists `begin`;
drop table if exists begin_test;