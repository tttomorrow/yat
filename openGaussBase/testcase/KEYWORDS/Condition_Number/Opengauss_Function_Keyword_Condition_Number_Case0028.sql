-- @testpoint: opengauss关键字condition_number(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists condition_number_test;
create table condition_number_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists condition_number;
create synonym condition_number for condition_number_test;
insert into condition_number values (1,'ada'),(2, 'bob');
update condition_number set condition_number.name='cici' where condition_number.id=2;
select * from condition_number;
drop synonym if exists condition_number;
--关键字带双引号-成功
drop synonym if exists "condition_number";
create synonym "condition_number" for condition_number_test;
drop synonym if exists "condition_number";

--关键字带单引号-合理报错
drop synonym if exists 'condition_number';
create synonym 'condition_number' for condition_number_test;
insert into 'condition_number' values (1,'ada'),(2, 'bob');
update 'condition_number' set 'condition_number'.name='cici' where 'condition_number'.id=2;
select * from 'condition_number';

--关键字带反引号-合理报错
drop synonym if exists `condition_number`;
create synonym `condition_number` for condition_number_test;
insert into `condition_number` values (1,'ada'),(2, 'bob');
update `condition_number` set `condition_number`.name='cici' where `condition_number`.id=2;
select * from `condition_number`;
drop table if exists condition_number_test;