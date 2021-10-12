-- @testpoint: opengauss关键字exists(非保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists exists_test;
create table exists_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists exists;
create synonym exists for exists_test;
insert into exists values (1,'ada'),(2, 'bob');
update exists set exists.name='cici' where exists.id=2;
select * from exists;
drop synonym if exists exists;

--关键字带双引号-成功
drop synonym if exists "exists";
create synonym "exists" for exists_test;
drop synonym if exists "exists";

--关键字带单引号-合理报错
drop synonym if exists 'exists';
create synonym 'exists' for exists_test;
insert into 'exists' values (1,'ada'),(2, 'bob');
update 'exists' set 'exists'.name='cici' where 'exists'.id=2;
select * from 'exists';

--关键字带反引号-合理报错
drop synonym if exists `exists`;
create synonym `exists` for exists_test;
insert into `exists` values (1,'ada'),(2, 'bob');
update `exists` set `exists`.name='cici' where `exists`.id=2;
select * from `exists`;
drop table if exists exists_test;