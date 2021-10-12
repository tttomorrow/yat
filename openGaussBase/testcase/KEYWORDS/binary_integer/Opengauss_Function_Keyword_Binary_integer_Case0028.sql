-- @testpoint: opengauss关键字binary_integer(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists binary_integer_test;
create table binary_integer_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists binary_integer;
create synonym binary_integer for binary_integer_test;
insert into binary_integer values (1,'ada'),(2, 'bob');
update binary_integer set binary_integer.name='cici' where binary_integer.id=2;
select * from binary_integer;

--清理环境
drop synonym if exists binary_integer;

--关键字带双引号-成功
drop synonym if exists "binary_integer";
create synonym "binary_integer" for binary_integer_test;
insert into "binary_integer" values (1,'ada'),(2, 'bob');
update "binary_integer" set "binary_integer".name='cici' where "binary_integer".id=2;
select * from "binary_integer";

--清理环境
drop synonym if exists "binary_integer";

--关键字带单引号-合理报错
drop synonym if exists 'binary_integer';

--关键字带反引号-合理报错
drop synonym if exists `binary_integer`;
drop table if exists binary_integer_test;