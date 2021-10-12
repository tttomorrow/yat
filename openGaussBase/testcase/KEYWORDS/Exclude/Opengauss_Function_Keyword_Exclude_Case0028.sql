-- @testpoint: opengauss关键字exclude(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists exclude_test;
create table exclude_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists exclude;
create synonym exclude for exclude_test;
insert into exclude values (1,'ada'),(2, 'bob');
update exclude set exclude.name='cici' where exclude.id=2;
select * from exclude;
drop synonym if exists exclude;

--关键字带双引号-成功
drop synonym if exists "exclude";
create synonym "exclude" for exclude_test;
drop synonym if exists "exclude";

--关键字带单引号-合理报错
drop synonym if exists 'exclude';
create synonym 'exclude' for exclude_test;
insert into 'exclude' values (1,'ada'),(2, 'bob');
update 'exclude' set 'exclude'.name='cici' where 'exclude'.id=2;
select * from 'exclude';

--关键字带反引号-合理报错
drop synonym if exists `exclude`;
create synonym `exclude` for exclude_test;
insert into `exclude` values (1,'ada'),(2, 'bob');
update `exclude` set `exclude`.name='cici' where `exclude`.id=2;
select * from `exclude`;
drop table if exists exclude_test;