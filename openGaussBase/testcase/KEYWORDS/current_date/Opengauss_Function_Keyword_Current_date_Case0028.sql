-- @testpoint: opengauss关键字current_date(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists current_date_test;
create table current_date_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists current_date;
create synonym current_date for current_date_test;


--关键字带双引号-成功
drop synonym if exists "current_date";
create synonym "current_date" for current_date_test;
insert into "current_date" values (1,'ada'),(2, 'bob');
update "current_date" set "current_date".name='cici' where "current_date".id=2;
select * from "current_date";

--清理环境
drop synonym "current_date";

--关键字带单引号-合理报错
drop synonym if exists 'current_date';
create synonym 'current_date' for current_date_test;
insert into 'current_date' values (1,'ada'),(2, 'bob');
update 'current_date' set 'current_date'.name='cici' where 'current_date'.id=2;
select * from 'current_date';

--关键字带反引号-合理报错
drop synonym if exists `current_date`;
create synonym `current_date` for current_date_test;
insert into `current_date` values (1,'ada'),(2, 'bob');
update `current_date` set `current_date`.name='cici' where `current_date`.id=2;
select * from `current_date`;
drop table if exists current_date_test;