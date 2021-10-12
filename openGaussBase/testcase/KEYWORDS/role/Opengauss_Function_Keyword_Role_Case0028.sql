-- @testpoint: opengauss关键字role(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists role_test;
create table role_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists role;
create synonym role for role_test;
insert into role values (1,'ada'),(2, 'bob');
update role set role.name='cici' where role.id=2;
select * from role;

--清理环境
drop synonym if exists role;

--关键字带双引号-成功
drop synonym if exists "role";
create synonym "role" for role_test;
insert into "role" values (1,'ada'),(2, 'bob');
update "role" set "role".name='cici' where "role".id=2;
select * from "role";

--清理环境
drop synonym if exists "role";

--关键字带单引号-合理报错
drop synonym if exists 'role';

--关键字带反引号-合理报错
drop synonym if exists `role`;
drop table if exists role_test;