-- @testpoint: opengauss关键字cycle(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists cycle_test;
create table cycle_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists cycle;
create synonym cycle for cycle_test;
insert into cycle values (1,'ada'),(2, 'bob');
update cycle set cycle.name='cici' where cycle.id=2;
select * from cycle;
drop synonym if exists cycle;

--关键字带双引号-成功
drop synonym if exists "cycle";
create synonym "cycle" for cycle_test;
drop synonym if exists "cycle";

--关键字带单引号-合理报错
drop synonym if exists 'cycle';
create synonym 'cycle' for cycle_test;
insert into 'cycle' values (1,'ada'),(2, 'bob');
update 'cycle' set 'cycle'.name='cici' where 'cycle'.id=2;
select * from 'cycle';

--关键字带反引号-合理报错
drop synonym if exists `cycle`;
create synonym `cycle` for cycle_test;
insert into `cycle` values (1,'ada'),(2, 'bob');
update `cycle` set `cycle`.name='cici' where `cycle`.id=2;
select * from `cycle`;
drop table if exists cycle_test;