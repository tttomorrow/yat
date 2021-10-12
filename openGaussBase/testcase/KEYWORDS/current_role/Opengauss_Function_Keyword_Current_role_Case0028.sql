-- @testpoint: opengauss关键字current_role(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists current_role_test;
create table current_role_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists current_role;
create synonym current_role for current_role_test;


--关键字带双引号-成功
drop synonym if exists "current_role";
create synonym "current_role" for current_role_test;
insert into "current_role" values (1,'ada'),(2, 'bob');
update "current_role" set "current_role".name='cici' where "current_role".id=2;
select * from "current_role";

--清理环境
drop synonym "current_role";

--关键字带单引号-合理报错
drop synonym if exists 'current_role';
create synonym 'current_role' for current_role_test;
insert into 'current_role' values (1,'ada'),(2, 'bob');
update 'current_role' set 'current_role'.name='cici' where 'current_role'.id=2;
select * from 'current_role';

--关键字带反引号-合理报错
drop synonym if exists `current_role`;
create synonym `current_role` for current_role_test;
insert into `current_role` values (1,'ada'),(2, 'bob');
update `current_role` set `current_role`.name='cici' where `current_role`.id=2;
select * from `current_role`;
drop table if exists current_role_test;