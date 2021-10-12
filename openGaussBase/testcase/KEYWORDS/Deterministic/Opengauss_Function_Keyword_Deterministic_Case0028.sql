-- @testpoint: opengauss关键字deterministic(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists deterministic_test;
create table deterministic_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists deterministic;
create synonym deterministic for deterministic_test;
insert into deterministic values (1,'ada'),(2, 'bob');
update deterministic set deterministic.name='cici' where deterministic.id=2;
select * from deterministic;
drop synonym if exists deterministic;

--关键字带双引号-成功
drop synonym if exists "deterministic";
create synonym "deterministic" for deterministic_test;
drop synonym if exists "deterministic";

--关键字带单引号-合理报错
drop synonym if exists 'deterministic';
create synonym 'deterministic' for deterministic_test;
insert into 'deterministic' values (1,'ada'),(2, 'bob');
update 'deterministic' set 'deterministic'.name='cici' where 'deterministic'.id=2;
select * from 'deterministic';

--关键字带反引号-合理报错
drop synonym if exists `deterministic`;
create synonym `deterministic` for deterministic_test;
insert into `deterministic` values (1,'ada'),(2, 'bob');
update `deterministic` set `deterministic`.name='cici' where `deterministic`.id=2;
select * from `deterministic`;
drop table if exists deterministic_test;