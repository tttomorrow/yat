-- @testpoint: opengauss关键字barrier(非保留)，作为同义词对象名,部分测试点合理报错
--前置条件
drop table if exists barrier_test;
create table barrier_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists barrier;
create synonym barrier for barrier_test;
insert into barrier values (1,'ada'),(2, 'bob');
update barrier set barrier.name='cici' where barrier.id=2;
select * from barrier;

--清理环境
drop synonym if exists barrier;

--关键字带双引号-成功
drop synonym if exists "barrier";
create synonym "barrier" for barrier_test;
insert into "barrier" values (1,'ada'),(2, 'bob');
update "barrier" set "barrier".name='cici' where "barrier".id=2;
select * from "barrier";

--清理环境
drop synonym if exists "barrier";

--关键字带单引号-合理报错
drop synonym if exists 'barrier';

--关键字带反引号-合理报错
drop synonym if exists `barrier`;
drop table if exists barrier_test;