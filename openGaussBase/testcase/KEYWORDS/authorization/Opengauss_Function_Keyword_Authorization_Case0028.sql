-- @testpoint: opengauss关键字Authorization(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists Authorization_test;
create table Authorization_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists Authorization;
create synonym Authorization for Authorization_test;


--关键字带双引号-成功
drop synonym if exists "Authorization";
create synonym "Authorization" for Authorization_test;
insert into "Authorization" values (1,'ada'),(2, 'bob');
update "Authorization" set "Authorization".name='cici' where "Authorization".id=2;
select * from "Authorization";

--清理环境
drop synonym "Authorization";

--关键字带单引号-合理报错
drop synonym if exists 'Authorization';
create synonym 'Authorization' for Authorization_test;
insert into 'Authorization' values (1,'ada'),(2, 'bob');
update 'Authorization' set 'Authorization'.name='cici' where 'Authorization'.id=2;
select * from 'Authorization';

--关键字带反引号-合理报错
drop synonym if exists `Authorization`;
create synonym `Authorization` for Authorization_test;
insert into `Authorization` values (1,'ada'),(2, 'bob');
update `Authorization` set `Authorization`.name='cici' where `Authorization`.id=2;
select * from `Authorization`;
drop table if exists Authorization_test;