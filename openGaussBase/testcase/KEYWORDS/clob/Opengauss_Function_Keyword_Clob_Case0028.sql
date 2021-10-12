-- @testpoint: opengauss关键字clob(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists clob_test;
create table clob_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists clob;
create synonym clob for clob_test;
insert into clob values (1,'ada'),(2, 'bob');
update clob set clob.name='cici' where clob.id=2;
select * from clob;

--清理环境
drop synonym if exists clob;

--关键字带双引号-成功
drop synonym if exists "clob";
create synonym "clob" for clob_test;
insert into "clob" values (1,'ada'),(2, 'bob');
update "clob" set "clob".name='cici' where "clob".id=2;
select * from "clob";

--清理环境
drop synonym if exists "clob";

--关键字带单引号-合理报错
drop synonym if exists 'clob';

--关键字带反引号-合理报错
drop synonym if exists `clob`;
drop table if exists clob_test;