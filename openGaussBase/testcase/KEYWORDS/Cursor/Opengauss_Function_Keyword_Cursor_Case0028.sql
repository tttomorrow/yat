-- @testpoint: opengauss关键字cursor(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists cursor_test;
create table cursor_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists cursor;
create synonym cursor for cursor_test;
insert into cursor values (1,'ada'),(2, 'bob');
update cursor set cursor.name='cici' where cursor.id=2;
select * from cursor;
drop synonym if exists cursor;
--关键字带双引号-成功
drop synonym if exists "cursor";
create synonym "cursor" for cursor_test;
drop synonym if exists "cursor";

--关键字带单引号-合理报错
drop synonym if exists 'cursor';
create synonym 'cursor' for cursor_test;
insert into 'cursor' values (1,'ada'),(2, 'bob');
update 'cursor' set 'cursor'.name='cici' where 'cursor'.id=2;
select * from 'cursor';

--关键字带反引号-合理报错
drop synonym if exists `cursor`;
create synonym `cursor` for cursor_test;
insert into `cursor` values (1,'ada'),(2, 'bob');
update `cursor` set `cursor`.name='cici' where `cursor`.id=2;
select * from `cursor`;
drop table if exists cursor_test;