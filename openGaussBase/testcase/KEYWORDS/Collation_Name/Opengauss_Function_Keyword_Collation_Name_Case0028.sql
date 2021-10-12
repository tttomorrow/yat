-- @testpoint: opengauss关键字collation_name(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists collation_name_test;
create table collation_name_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists collation_name;
create synonym collation_name for collation_name_test;
insert into collation_name values (1,'ada'),(2, 'bob');
update collation_name set collation_name.name='cici' where collation_name.id=2;
select * from collation_name;
drop synonym if exists collation_name;
--关键字带双引号-成功
drop synonym if exists "collation_name";
create synonym "collation_name" for collation_name_test;
drop synonym if exists "collation_name";

--关键字带单引号-合理报错
drop synonym if exists 'collation_name';
create synonym 'collation_name' for collation_name_test;
insert into 'collation_name' values (1,'ada'),(2, 'bob');
update 'collation_name' set 'collation_name'.name='cici' where 'collation_name'.id=2;
select * from 'collation_name';

--关键字带反引号-合理报错
drop synonym if exists `collation_name`;
create synonym `collation_name` for collation_name_test;
insert into `collation_name` values (1,'ada'),(2, 'bob');
update `collation_name` set `collation_name`.name='cici' where `collation_name`.id=2;
select * from `collation_name`;
drop table if exists collation_name_test;