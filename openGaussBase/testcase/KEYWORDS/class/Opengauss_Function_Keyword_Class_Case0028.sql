-- @testpoint: opengauss关键字class(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists class_test;
create table class_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists class;
create synonym class for class_test;
insert into class values (1,'ada'),(2, 'bob');
update class set class.name='cici' where class.id=2;
select * from class;

--清理环境
drop synonym if exists class;

--关键字带双引号-成功
drop synonym if exists "class";
create synonym "class" for class_test;
insert into "class" values (1,'ada'),(2, 'bob');
update "class" set "class".name='cici' where "class".id=2;
select * from "class";

--清理环境
drop synonym if exists "class";

--关键字带单引号-合理报错
drop synonym if exists 'class';

--关键字带反引号-合理报错
drop synonym if exists `class`;
drop table if exists class_test;