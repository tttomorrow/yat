-- @testpoint: opengauss关键字per(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists per_test;
create table per_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists per;
create synonym per for per_test;
insert into per values (1,'ada'),(2, 'bob');
update per set per.name='cici' where per.id=2;
select * from per;

--关键字带双引号-成功
drop synonym if exists "per";
create synonym "per" for per_test;


--关键字带单引号-合理报错
drop synonym if exists 'per';
create synonym 'per' for per_test;
insert into 'per' values (1,'ada'),(2, 'bob');
update 'per' set 'per'.name='cici' where 'per'.id=2;
select * from 'per';

--关键字带反引号-合理报错
drop synonym if exists `per`;
create synonym `per` for per_test;
insert into `per` values (1,'ada'),(2, 'bob');
update `per` set `per`.name='cici' where `per`.id=2;
select * from `per`;
--清理环境
drop synonym if exists "per";
drop synonym if exists per;
drop table if exists per_test;