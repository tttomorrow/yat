-- @testpoint: opengauss关键字binary_double(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists binary_double_test;
create table binary_double_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists binary_double;
create synonym binary_double for binary_double_test;
insert into binary_double values (1,'ada'),(2, 'bob');
update binary_double set binary_double.name='cici' where binary_double.id=2;
select * from binary_double;

--清理环境
drop synonym if exists binary_double;

--关键字带双引号-成功
drop synonym if exists "binary_double";
create synonym "binary_double" for binary_double_test;
insert into "binary_double" values (1,'ada'),(2, 'bob');
update "binary_double" set "binary_double".name='cici' where "binary_double".id=2;
select * from "binary_double";

--清理环境
drop synonym if exists "binary_double";

--关键字带单引号-合理报错
drop synonym if exists 'binary_double';

--关键字带反引号-合理报错
drop synonym if exists `binary_double`;
drop table if exists binary_double_test;