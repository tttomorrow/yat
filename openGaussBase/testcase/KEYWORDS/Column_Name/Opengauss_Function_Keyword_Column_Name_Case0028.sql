-- @testpoint: opengauss关键字column_name(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists column_name_test;
create table column_name_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists column_name;
create synonym column_name for column_name_test;
insert into column_name values (1,'ada'),(2, 'bob');
update column_name set column_name.name='cici' where column_name.id=2;
select * from column_name;
drop synonym if exists column_name;
--关键字带双引号-成功
drop synonym if exists "column_name";
create synonym "column_name" for column_name_test;
drop synonym if exists "column_name";

--关键字带单引号-合理报错
drop synonym if exists 'column_name';
create synonym 'column_name' for column_name_test;
insert into 'column_name' values (1,'ada'),(2, 'bob');
update 'column_name' set 'column_name'.name='cici' where 'column_name'.id=2;
select * from 'column_name';

--关键字带反引号-合理报错
drop synonym if exists `column_name`;
create synonym `column_name` for column_name_test;
insert into `column_name` values (1,'ada'),(2, 'bob');
update `column_name` set `column_name`.name='cici' where `column_name`.id=2;
select * from `column_name`;
drop table if exists column_name_test;