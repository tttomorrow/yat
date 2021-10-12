-- @testpoint: opengauss关键字bigint(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists bigint_test;
create table bigint_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists bigint;
create synonym bigint for bigint_test;
insert into bigint values (1,'ada'),(2, 'bob');
update bigint set bigint.name='cici' where bigint.id=2;
select * from bigint;

--清理环境
drop synonym if exists bigint;

--关键字带双引号-成功
drop synonym if exists "bigint";
create synonym "bigint" for bigint_test;
insert into "bigint" values (1,'ada'),(2, 'bob');
update "bigint" set "bigint".name='cici' where "bigint".id=2;
select * from "bigint";

--清理环境
drop synonym if exists "bigint";

--关键字带单引号-合理报错
drop synonym if exists 'bigint';

--关键字带反引号-合理报错
drop synonym if exists `bigint`;
drop table if exists bigint_test;