-- @testpoint: opengauss关键字called(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists called_test;
create table called_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists called;
create synonym called for called_test;
insert into called values (1,'ada'),(2, 'bob');
update called set called.name='cici' where called.id=2;
select * from called;

--清理环境
drop synonym if exists called;

--关键字带双引号-成功
drop synonym if exists "called";
create synonym "called" for called_test;
insert into "called" values (1,'ada'),(2, 'bob');
update "called" set "called".name='cici' where "called".id=2;
select * from "called";

--清理环境
drop synonym if exists "called";

--关键字带单引号-合理报错
drop synonym if exists 'called';

--关键字带反引号-合理报错
drop synonym if exists `called`;
drop table if exists called_test;