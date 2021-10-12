-- @testpoint: opengauss关键字condition(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists condition_test;
create table condition_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists condition;
create synonym condition for condition_test;
insert into condition values (1,'ada'),(2, 'bob');
update condition set condition.name='cici' where condition.id=2;
select * from condition;
drop synonym if exists condition;
--关键字带双引号-成功
drop synonym if exists "condition";
create synonym "condition" for condition_test;
drop synonym if exists "condition";

--关键字带单引号-合理报错
drop synonym if exists 'condition';
create synonym 'condition' for condition_test;
insert into 'condition' values (1,'ada'),(2, 'bob');
update 'condition' set 'condition'.name='cici' where 'condition'.id=2;
select * from 'condition';

--关键字带反引号-合理报错
drop synonym if exists `condition`;
create synonym `condition` for condition_test;
insert into `condition` values (1,'ada'),(2, 'bob');
update `condition` set `condition`.name='cici' where `condition`.id=2;
select * from `condition`;
drop table if exists condition_test;