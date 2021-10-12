-- @testpoint: opengauss关键字in(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists in_test;
create table in_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists in;
create synonym in for in_test;


--关键字带双引号-成功
drop synonym if exists "in";
create synonym "in" for in_test;
insert into "in" values (1,'ada'),(2, 'bob');
update "in" set "in".name='cici' where "in".id=2;
select * from "in";

--清理环境
drop synonym "in";

--关键字带单引号-合理报错
drop synonym if exists 'in';
create synonym 'in' for in_test;
insert into 'in' values (1,'ada'),(2, 'bob');
update 'in' set 'in'.name='cici' where 'in'.id=2;
select * from 'in';

--关键字带反引号-合理报错
drop synonym if exists `in`;
create synonym `in` for in_test;
insert into `in` values (1,'ada'),(2, 'bob');
update `in` set `in`.name='cici' where `in`.id=2;
select * from `in`;
--清理环境
drop table if exists in_test cascade;