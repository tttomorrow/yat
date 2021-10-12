-- @testpoint: opengauss关键字diagnostics(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists diagnostics_test;
create table diagnostics_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists diagnostics;
create synonym diagnostics for diagnostics_test;
insert into diagnostics values (1,'ada'),(2, 'bob');
update diagnostics set diagnostics.name='cici' where diagnostics.id=2;
select * from diagnostics;
drop synonym if exists diagnostics;

--关键字带双引号-成功
drop synonym if exists "diagnostics";
create synonym "diagnostics" for diagnostics_test;
drop synonym if exists "diagnostics";

--关键字带单引号-合理报错
drop synonym if exists 'diagnostics';
create synonym 'diagnostics' for diagnostics_test;
insert into 'diagnostics' values (1,'ada'),(2, 'bob');
update 'diagnostics' set 'diagnostics'.name='cici' where 'diagnostics'.id=2;
select * from 'diagnostics';

--关键字带反引号-合理报错
drop synonym if exists `diagnostics`;
create synonym `diagnostics` for diagnostics_test;
insert into `diagnostics` values (1,'ada'),(2, 'bob');
update `diagnostics` set `diagnostics`.name='cici' where `diagnostics`.id=2;
select * from `diagnostics`;
drop table if exists diagnostics_test;