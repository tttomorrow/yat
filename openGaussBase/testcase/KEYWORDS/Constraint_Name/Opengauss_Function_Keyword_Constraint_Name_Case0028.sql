-- @testpoint: opengauss关键字constraint_name(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists constraint_name_test;
create table constraint_name_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists constraint_name;
create synonym constraint_name for constraint_name_test;
insert into constraint_name values (1,'ada'),(2, 'bob');
update constraint_name set constraint_name.name='cici' where constraint_name.id=2;
select * from constraint_name;

--关键字带双引号-成功
drop synonym if exists "constraint_name";
create synonym "constraint_name" for constraint_name_test;


--关键字带单引号-合理报错
drop synonym if exists 'constraint_name';
create synonym 'constraint_name' for constraint_name_test;
insert into 'constraint_name' values (1,'ada'),(2, 'bob');
update 'constraint_name' set 'constraint_name'.name='cici' where 'constraint_name'.id=2;
select * from 'constraint_name';

--关键字带反引号-合理报错
drop synonym if exists `constraint_name`;
create synonym `constraint_name` for constraint_name_test;
insert into `constraint_name` values (1,'ada'),(2, 'bob');
update `constraint_name` set `constraint_name`.name='cici' where `constraint_name`.id=2;
select * from `constraint_name`;

--清理环境
drop synonym if exists constraint_name;
drop synonym if exists "constraint_name";
drop table if exists constraint_name_test;