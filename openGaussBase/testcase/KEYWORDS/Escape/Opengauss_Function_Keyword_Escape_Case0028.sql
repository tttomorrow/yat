-- @testpoint: opengauss关键字escape(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists escape_test;
create table escape_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists escape;
create synonym escape for escape_test;
insert into escape values (1,'ada'),(2, 'bob');
update escape set escape.name='cici' where escape.id=2;
select * from escape;
drop synonym if exists escape;

--关键字带双引号-成功
drop synonym if exists "escape";
create synonym "escape" for escape_test;
drop synonym if exists "escape";

--关键字带单引号-合理报错
drop synonym if exists 'escape';
create synonym 'escape' for escape_test;
insert into 'escape' values (1,'ada'),(2, 'bob');
update 'escape' set 'escape'.name='cici' where 'escape'.id=2;
select * from 'escape';

--关键字带反引号-合理报错
drop synonym if exists `escape`;
create synonym `escape` for escape_test;
insert into `escape` values (1,'ada'),(2, 'bob');
update `escape` set `escape`.name='cici' where `escape`.id=2;
select * from `escape`;
drop table if exists escape_test;