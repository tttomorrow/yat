-- @testpoint: opengauss关键字localtime(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists localtime_test;
create table localtime_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists localtime;
create synonym localtime for localtime_test;


--关键字带双引号-成功
drop synonym if exists "localtime";
create synonym "localtime" for localtime_test;
insert into "localtime" values (1,'ada'),(2, 'bob');
update "localtime" set "localtime".name='cici' where "localtime".id=2;
select * from "localtime";

--清理环境
drop synonym "localtime";

--关键字带单引号-合理报错
drop synonym if exists 'localtime';
create synonym 'localtime' for localtime_test;
insert into 'localtime' values (1,'ada'),(2, 'bob');
update 'localtime' set 'localtime'.name='cici' where 'localtime'.id=2;
select * from 'localtime';

--关键字带反引号-合理报错
drop synonym if exists `localtime`;
create synonym `localtime` for localtime_test;
insert into `localtime` values (1,'ada'),(2, 'bob');
update `localtime` set `localtime`.name='cici' where `localtime`.id=2;
select * from `localtime`;
--清理环境
drop table if exists localtime_test cascade;