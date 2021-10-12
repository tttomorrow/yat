-- @testpoint: opengauss关键字rebuild(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists rebuild_test;
create table rebuild_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists rebuild;
create synonym rebuild for rebuild_test;
insert into rebuild values (1,'ada'),(2, 'bob');
update rebuild set rebuild.name='cici' where rebuild.id=2;
select * from rebuild;
drop synonym if exists rebuild;

--关键字带双引号-成功
drop synonym if exists "rebuild";
create synonym "rebuild" for rebuild_test;
insert into "rebuild" values (1,'ada'),(2, 'bob');
update "rebuild" set "rebuild".name='cici' where "rebuild".id=2;
select * from "rebuild";
drop synonym if exists "rebuild";

--关键字带单引号-合理报错
drop synonym if exists 'rebuild';

--关键字带反引号-合理报错
drop synonym if exists `rebuild`;
drop table if exists rebuild_test;