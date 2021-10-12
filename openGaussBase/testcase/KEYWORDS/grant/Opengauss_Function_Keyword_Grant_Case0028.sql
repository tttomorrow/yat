-- @testpoint: opengauss关键字grant(保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists grant_test;
create table grant_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists grant;
create synonym grant for grant_test;


--关键字带双引号-成功
drop synonym if exists "grant";
create synonym "grant" for grant_test;
insert into "grant" values (1,'ada'),(2, 'bob');
update "grant" set "grant".name='cici' where "grant".id=2;
select * from "grant";

--清理环境
drop synonym "grant";

--关键字带单引号-合理报错
drop synonym if exists 'grant';
create synonym 'grant' for grant_test;
insert into 'grant' values (1,'ada'),(2, 'bob');
update 'grant' set 'grant'.name='cici' where 'grant'.id=2;
select * from 'grant';

--关键字带反引号-合理报错
drop synonym if exists `grant`;
create synonym `grant` for grant_test;
insert into `grant` values (1,'ada'),(2, 'bob');
update `grant` set `grant`.name='cici' where `grant`.id=2;
select * from `grant`;

--清理环境
drop table if exists grant_test;