-- @testpoint: opengauss关键字performance(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists performance_test;
create table performance_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists performance;
create synonym performance for performance_test;


--关键字带双引号-成功
drop synonym if exists "performance";
create synonym "performance" for performance_test;
insert into "performance" values (1,'ada'),(2, 'bob');
update "performance" set "performance".name='cici' where "performance".id=2;
select * from "performance";

--清理环境
drop synonym "performance";

--关键字带单引号-合理报错
drop synonym if exists 'performance';
create synonym 'performance' for performance_test;
insert into 'performance' values (1,'ada'),(2, 'bob');
update 'performance' set 'performance'.name='cici' where 'performance'.id=2;
select * from 'performance';

--关键字带反引号-合理报错
drop synonym if exists `performance`;
create synonym `performance` for performance_test;
insert into `performance` values (1,'ada'),(2, 'bob');
update `performance` set `performance`.name='cici' where `performance`.id=2;
select * from `performance`;
--清理环境
drop table if exists performance_test cascade;