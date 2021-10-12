-- @testpoint: opengauss关键字cursor_name(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists cursor_name_test;
create table cursor_name_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists cursor_name;
create synonym cursor_name for cursor_name_test;
insert into cursor_name values (1,'ada'),(2, 'bob');
update cursor_name set cursor_name.name='cici' where cursor_name.id=2;
select * from cursor_name;
drop synonym if exists cursor_name;

--关键字带双引号-成功
drop synonym if exists "cursor_name";
create synonym "cursor_name" for cursor_name_test;
drop synonym if exists "cursor_name";

--关键字带单引号-合理报错
drop synonym if exists 'cursor_name';
create synonym 'cursor_name' for cursor_name_test;
insert into 'cursor_name' values (1,'ada'),(2, 'bob');
update 'cursor_name' set 'cursor_name'.name='cici' where 'cursor_name'.id=2;
select * from 'cursor_name';

--关键字带反引号-合理报错
drop synonym if exists `cursor_name`;
create synonym `cursor_name` for cursor_name_test;
insert into `cursor_name` values (1,'ada'),(2, 'bob');
update `cursor_name` set `cursor_name`.name='cici' where `cursor_name`.id=2;
select * from `cursor_name`;
drop table if exists cursor_name_test;