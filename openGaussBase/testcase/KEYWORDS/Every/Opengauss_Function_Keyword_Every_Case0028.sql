-- @testpoint: opengauss关键字every(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists every_test;
create table every_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists every;
create synonym every for every_test;
insert into every values (1,'ada'),(2, 'bob');
update every set every.name='cici' where every.id=2;
select * from every;
drop synonym if exists every;

--关键字带双引号-成功
drop synonym if exists "every";
create synonym "every" for every_test;
drop synonym if exists "every";

--关键字带单引号-合理报错
drop synonym if exists 'every';
create synonym 'every' for every_test;
insert into 'every' values (1,'ada'),(2, 'bob');
update 'every' set 'every'.name='cici' where 'every'.id=2;
select * from 'every';

--关键字带反引号-合理报错
drop synonym if exists `every`;
create synonym `every` for every_test;
insert into `every` values (1,'ada'),(2, 'bob');
update `every` set `every`.name='cici' where `every`.id=2;
select * from `every`;
drop table if exists every_test;