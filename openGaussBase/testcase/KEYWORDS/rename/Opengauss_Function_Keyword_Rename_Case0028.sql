-- @testpoint: opengauss关键字rename(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists rename_test;
create table rename_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists rename;
create synonym rename for rename_test;
insert into rename values (1,'ada'),(2, 'bob');
update rename set rename.name='cici' where rename.id=2;
select * from rename;
drop synonym if exists rename;

--关键字带双引号-成功
drop synonym if exists "rename";
create synonym "rename" for rename_test;
insert into "rename" values (1,'ada'),(2, 'bob');
update "rename" set "rename".name='cici' where "rename".id=2;
select * from "rename";
drop synonym if exists "rename";

--关键字带单引号-合理报错
drop synonym if exists 'rename';

--关键字带反引号-合理报错
drop synonym if exists `rename`;
drop table if exists rename_test;