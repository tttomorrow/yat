-- @testpoint: opengauss关键字Interval(非保留)，作为同义词对象名 合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-创建成功
drop synonym if exists Interval;
create synonym Interval for explain_test;
insert into Interval values (1,'ada'),(2, 'bob');
update Interval set Interval.name='cici' where Interval.id=2;
select * from Interval;

--关键字带双引号-创建成功
drop synonym if exists "Interval";
create synonym "Interval" for explain_test;

--关键字带单引号-合理报错
drop synonym if exists 'Interval';
create synonym 'Interval' for explain_test;
insert into 'Interval' values (1,'ada'),(2, 'bob');
update 'Interval' set 'Interval'.name='cici' where 'Interval'.id=2;
select * from 'Interval';

--关键字带反引号-合理报错
drop synonym if exists `Interval`;
create synonym `Interval` for explain_test;
insert into `Interval` values (1,'ada'),(2, 'bob');
update `Interval` set `Interval`.name='cici' where `Interval`.id=2;
select * from `Interval`;

--清理环境
drop synonym if exists Interval;
drop synonym if exists "Interval";
drop table if exists explain_test;