-- @testpoint: opengauss关键字create(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists create_test;
create table create_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists create;
create synonym create for create_test;


--关键字带双引号-成功
drop synonym if exists "create";
create synonym "create" for create_test;
insert into "create" values (1,'ada'),(2, 'bob');
update "create" set "create".name='cici' where "create".id=2;
select * from "create";

--清理环境
drop synonym "create";

--关键字带单引号-合理报错
drop synonym if exists 'create';
create synonym 'create' for create_test;
insert into 'create' values (1,'ada'),(2, 'bob');
update 'create' set 'create'.name='cici' where 'create'.id=2;
select * from 'create';

--关键字带反引号-合理报错
drop synonym if exists `create`;
create synonym `create` for create_test;
insert into `create` values (1,'ada'),(2, 'bob');
update `create` set `create`.name='cici' where `create`.id=2;
select * from `create`;
drop table if exists create_test;