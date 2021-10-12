-- @testpoint: opengauss关键字close(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists close_test;
create table close_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists close;
create synonym close for close_test;
insert into close values (1,'ada'),(2, 'bob');
update close set close.name='cici' where close.id=2;
select * from close;

--清理环境
drop synonym if exists close;

--关键字带双引号-成功
drop synonym if exists "close";
create synonym "close" for close_test;
insert into "close" values (1,'ada'),(2, 'bob');
update "close" set "close".name='cici' where "close".id=2;
select * from "close";

--清理环境
drop synonym if exists "close";

--关键字带单引号-合理报错
drop synonym if exists 'close';

--关键字带反引号-合理报错
drop synonym if exists `close`;
drop table if exists close_test;