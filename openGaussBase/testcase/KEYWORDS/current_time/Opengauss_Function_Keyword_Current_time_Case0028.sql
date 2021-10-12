-- @testpoint: opengauss关键字current_time(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists current_time_test;
create table current_time_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists current_time;
create synonym current_time for current_time_test;


--关键字带双引号-成功
drop synonym if exists "current_time";
create synonym "current_time" for current_time_test;
insert into "current_time" values (1,'ada'),(2, 'bob');
update "current_time" set "current_time".name='cici' where "current_time".id=2;
select * from "current_time";

--清理环境
drop synonym "current_time";

--关键字带单引号-合理报错
drop synonym if exists 'current_time';
create synonym 'current_time' for current_time_test;
insert into 'current_time' values (1,'ada'),(2, 'bob');
update 'current_time' set 'current_time'.name='cici' where 'current_time'.id=2;
select * from 'current_time';

--关键字带反引号-合理报错
drop synonym if exists `current_time`;
create synonym `current_time` for current_time_test;
insert into `current_time` values (1,'ada'),(2, 'bob');
update `current_time` set `current_time`.name='cici' where `current_time`.id=2;
select * from `current_time`;
drop table if exists current_time_test;