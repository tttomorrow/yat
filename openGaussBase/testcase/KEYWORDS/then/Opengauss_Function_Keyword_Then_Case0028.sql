-- @testpoint: opengauss关键字then(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists then_test;
create table then_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists then;
create synonym then for then_test;


--关键字带双引号-成功
drop synonym if exists "then";
create synonym "then" for then_test;
insert into "then" values (1,'ada'),(2, 'bob');
update "then" set "then".name='cici' where "then".id=2;
select * from "then";
drop synonym "then";
--关键字带单引号-合理报错
drop synonym if exists 'then';
create synonym 'then' for then_test;
insert into 'then' values (1,'ada'),(2, 'bob');
update 'then' set 'then'.name='cici' where 'then'.id=2;
select * from 'then';

--关键字带反引号-合理报错
drop synonym if exists `then`;
create synonym `then` for then_test;
insert into `then` values (1,'ada'),(2, 'bob');
update `then` set `then`.name='cici' where `then`.id=2;
select * from `then`;

--清理环境
drop table if exists then_test;