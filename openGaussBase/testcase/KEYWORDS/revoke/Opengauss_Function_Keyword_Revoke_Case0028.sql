-- @testpoint: opengauss关键字revoke(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists revoke_test;
create table revoke_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists revoke;
create synonym revoke for revoke_test;
insert into revoke values (1,'ada'),(2, 'bob');
update revoke set revoke.name='cici' where revoke.id=2;
select * from revoke;

--清理环境
drop synonym if exists revoke;

--关键字带双引号-成功
drop synonym if exists "revoke";
create synonym "revoke" for revoke_test;
insert into "revoke" values (1,'ada'),(2, 'bob');
update "revoke" set "revoke".name='cici' where "revoke".id=2;
select * from "revoke";

--清理环境
drop synonym if exists "revoke";

--关键字带单引号-合理报错
drop synonym if exists 'revoke';

--关键字带反引号-合理报错
drop synonym if exists `revoke`;
drop table if exists revoke_test;