-- @testpoint: opengauss关键字standalone(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists standalone;
create synonym standalone for explain_test;
insert into standalone values (1,'ada'),(2, 'bob');
update standalone set standalone.name='cici' where standalone.id=2;
select * from standalone;
drop synonym if exists standalone;

--关键字带双引号-成功
drop synonym if exists "standalone";
create synonym "standalone" for explain_test;
drop synonym if exists "standalone";

--关键字带单引号-合理报错
drop synonym if exists 'standalone';
create synonym 'standalone' for explain_test;
insert into 'standalone' values (1,'ada'),(2, 'bob');
update 'standalone' set 'standalone'.name='cici' where 'standalone'.id=2;
select * from 'standalone';

--关键字带反引号-合理报错
drop synonym if exists `standalone`;
create synonym `standalone` for explain_test;
insert into `standalone` values (1,'ada'),(2, 'bob');
update `standalone` set `standalone`.name='cici' where `standalone`.id=2;
select * from `standalone`;
drop table if exists explain_test;