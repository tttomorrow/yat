-- @testpoint: opengauss关键字symmetric(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists symmetric_test;
create table symmetric_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists symmetric;
create synonym symmetric for symmetric_test;


--关键字带双引号-成功
drop synonym if exists "symmetric";
create synonym "symmetric" for symmetric_test;
insert into "symmetric" values (1,'ada'),(2, 'bob');
update "symmetric" set "symmetric".name='cici' where "symmetric".id=2;
select * from "symmetric";
drop synonym "symmetric";
--关键字带单引号-合理报错
drop synonym if exists 'symmetric';
create synonym 'symmetric' for symmetric_test;
insert into 'symmetric' values (1,'ada'),(2, 'bob');
update 'symmetric' set 'symmetric'.name='cici' where 'symmetric'.id=2;
select * from 'symmetric';

--关键字带反引号-合理报错
drop synonym if exists `symmetric`;
create synonym `symmetric` for symmetric_test;
insert into `symmetric` values (1,'ada'),(2, 'bob');
update `symmetric` set `symmetric`.name='cici' where `symmetric`.id=2;
select * from `symmetric`;

--清理环境
drop table if exists symmetric_test cascade;