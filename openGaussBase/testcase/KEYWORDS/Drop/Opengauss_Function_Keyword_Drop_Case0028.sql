-- @testpoint: opengauss关键字drop(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists drop_test;
create table drop_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists drop;
create synonym drop for drop_test;
insert into drop values (1,'ada'),(2, 'bob');
update drop set drop.name='cici' where drop.id=2;
select * from drop;
drop synonym if exists drop;

--关键字带双引号-成功
drop synonym if exists "drop";
create synonym "drop" for drop_test;
drop synonym if exists "drop";

--关键字带单引号-合理报错
drop synonym if exists 'drop';
create synonym 'drop' for drop_test;
insert into 'drop' values (1,'ada'),(2, 'bob');
update 'drop' set 'drop'.name='cici' where 'drop'.id=2;
select * from 'drop';

--关键字带反引号-合理报错
drop synonym if exists `drop`;
create synonym `drop` for drop_test;
insert into `drop` values (1,'ada'),(2, 'bob');
update `drop` set `drop`.name='cici' where `drop`.id=2;
select * from `drop`;
drop table if exists drop_test;