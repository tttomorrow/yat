-- @testpoint: opengauss关键字position(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists position_test;
create table position_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists position;
create synonym position for position_test;
insert into position values (1,'ada'),(2, 'bob');
update position set position.name='cici' where position.id=2;
select * from position;

--关键字带双引号-成功
drop synonym if exists "position";
create synonym "position" for position_test;


--关键字带单引号-合理报错
drop synonym if exists 'position';
create synonym 'position' for position_test;
insert into 'position' values (1,'ada'),(2, 'bob');
update 'position' set 'position'.name='cici' where 'position'.id=2;
select * from 'position';

--关键字带反引号-合理报错
drop synonym if exists `position`;
create synonym `position` for position_test;
insert into `position` values (1,'ada'),(2, 'bob');
update `position` set `position`.name='cici' where `position`.id=2;
select * from `position`;
--清理环境
drop synonym if exists "position";
drop synonym if exists position;
drop table if exists position_test;