-- @testpoint: opengauss关键字table_name(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists table_name;
create synonym table_name for explain_test;
insert into table_name values (1,'ada'),(2, 'bob');
update table_name set table_name.name='cici' where table_name.id=2;
select * from table_name;
drop synonym if exists table_name;

--关键字带双引号-成功
drop synonym if exists "table_name";
create synonym "table_name" for explain_test;
drop synonym if exists "table_name";

--关键字带单引号-合理报错
drop synonym if exists 'table_name';
create synonym 'table_name' for explain_test;
insert into 'table_name' values (1,'ada'),(2, 'bob');
update 'table_name' set 'table_name'.name='cici' where 'table_name'.id=2;
select * from 'table_name';

--关键字带反引号-合理报错
drop synonym if exists `table_name`;
create synonym `table_name` for explain_test;
insert into `table_name` values (1,'ada'),(2, 'bob');
update `table_name` set `table_name`.name='cici' where `table_name`.id=2;
select * from `table_name`;

--清理环境
drop table if exists explain_test;