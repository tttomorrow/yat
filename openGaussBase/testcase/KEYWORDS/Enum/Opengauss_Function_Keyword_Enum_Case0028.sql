-- @testpoint: opengauss关键字enum(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists enum_test;
create table enum_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists enum;
create synonym enum for enum_test;
insert into enum values (1,'ada'),(2, 'bob');
update enum set enum.name='cici' where enum.id=2;
select * from enum;
drop synonym if exists enum;

--关键字带双引号-成功
drop synonym if exists "enum";
create synonym "enum" for enum_test;
drop synonym if exists "enum";

--关键字带单引号-合理报错
drop synonym if exists 'enum';
create synonym 'enum' for enum_test;
insert into 'enum' values (1,'ada'),(2, 'bob');
update 'enum' set 'enum'.name='cici' where 'enum'.id=2;
select * from 'enum';

--关键字带反引号-合理报错
drop synonym if exists `enum`;
create synonym `enum` for enum_test;
insert into `enum` values (1,'ada'),(2, 'bob');
update `enum` set `enum`.name='cici' where `enum`.id=2;
select * from `enum`;
drop table if exists enum_test;