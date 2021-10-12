-- @testpoint: opengauss关键字binary(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists binary_test;
create table binary_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists binary;
create synonym binary for binary_test;
insert into binary values (1,'ada'),(2, 'bob');
update binary set binary.name='cici' where binary.id=2;
select * from binary;

--清理环境
drop synonym if exists binary;

--关键字带双引号-成功
drop synonym if exists "binary";
create synonym "binary" for binary_test;
insert into "binary" values (1,'ada'),(2, 'bob');
update "binary" set "binary".name='cici' where "binary".id=2;
select * from "binary";

--清理环境
drop synonym if exists "binary";

--关键字带单引号-合理报错
drop synonym if exists 'binary';

--关键字带反引号-合理报错
drop synonym if exists `binary`;
drop table if exists binary_test;