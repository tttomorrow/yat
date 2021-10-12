-- @testpoint: opengauss关键字class_origin(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists class_origin_test;
create table class_origin_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists class_origin;
create synonym class_origin for class_origin_test;
insert into class_origin values (1,'ada'),(2, 'bob');
update class_origin set class_origin.name='cici' where class_origin.id=2;
select * from class_origin;

--清理环境
drop synonym if exists class_origin;

--关键字带双引号-成功
drop synonym if exists "class_origin";
create synonym "class_origin" for class_origin_test;
insert into "class_origin" values (1,'ada'),(2, 'bob');
update "class_origin" set "class_origin".name='cici' where "class_origin".id=2;
select * from "class_origin";

--清理环境
drop synonym if exists "class_origin";

--关键字带单引号-合理报错
drop synonym if exists 'class_origin';

--关键字带反引号-合理报错
drop synonym if exists `class_origin`;
drop table if exists class_origin_test;