-- @testpoint: opengauss关键字privileges(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists privileges_test;
create table privileges_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists privileges;
create synonym privileges for privileges_test;
insert into privileges values (1,'ada'),(2, 'bob');
update privileges set privileges.name='cici' where privileges.id=2;
select * from privileges;
drop synonym if exists privileges;

--关键字带双引号-成功
drop synonym if exists "privileges";
create synonym "privileges" for privileges_test;
insert into "privileges" values (1,'ada'),(2, 'bob');
update "privileges" set "privileges".name='cici' where "privileges".id=2;
select * from "privileges";
drop synonym if exists "privileges";

--关键字带单引号-合理报错
drop synonym if exists 'privileges';

--关键字带反引号-合理报错
drop synonym if exists `privileges`;
--清理环境
drop synonym if exists privileges;
drop synonym if exists "privileges";
drop table if exists privileges_test;