-- @testpoint: opengauss关键字returned_sqlstate(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists returned_sqlstate_test;
create table returned_sqlstate_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists returned_sqlstate;
create synonym returned_sqlstate for returned_sqlstate_test;
insert into returned_sqlstate values (1,'ada'),(2, 'bob');
update returned_sqlstate set returned_sqlstate.name='cici' where returned_sqlstate.id=2;
select * from returned_sqlstate;

--清理环境
drop synonym if exists returned_sqlstate;

--关键字带双引号-成功
drop synonym if exists "returned_sqlstate";
create synonym "returned_sqlstate" for returned_sqlstate_test;
insert into "returned_sqlstate" values (1,'ada'),(2, 'bob');
update "returned_sqlstate" set "returned_sqlstate".name='cici' where "returned_sqlstate".id=2;
select * from "returned_sqlstate";

--清理环境
drop synonym if exists "returned_sqlstate";

--关键字带单引号-合理报错
drop synonym if exists 'returned_sqlstate';

--关键字带反引号-合理报错
drop synonym if exists `returned_sqlstate`;
drop table if exists returned_sqlstate_test;