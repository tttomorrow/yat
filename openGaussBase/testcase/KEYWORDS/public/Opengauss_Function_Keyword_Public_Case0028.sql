-- @testpoint: opengauss关键字public(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists public_test;
create table public_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists public;
create synonym public for public_test;
insert into public values (1,'ada'),(2, 'bob');
update public set public.name='cici' where public.id=2;
select * from public;
drop synonym if exists public;

--关键字带双引号-成功
drop synonym if exists "public";
create synonym "public" for public_test;
insert into "public" values (1,'ada'),(2, 'bob');
update "public" set "public".name='cici' where "public".id=2;
select * from "public";
drop synonym if exists "public";

--关键字带单引号-合理报错
drop synonym if exists 'public';

--关键字带反引号-合理报错
drop synonym if exists `public`;
--清理环境
drop table if exists public_test;