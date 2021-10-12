-- @testpoint: opengauss关键字blob(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists blob_test;
create table blob_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists blob;
create synonym blob for blob_test;
insert into blob values (1,'ada'),(2, 'bob');
update blob set blob.name='cici' where blob.id=2;
select * from blob;

--清理环境
drop synonym if exists blob;

--关键字带双引号-成功
drop synonym if exists "blob";
create synonym "blob" for blob_test;
insert into "blob" values (1,'ada'),(2, 'bob');
update "blob" set "blob".name='cici' where "blob".id=2;
select * from "blob";

--清理环境
drop synonym if exists "blob";

--关键字带单引号-合理报错
drop synonym if exists 'blob';

--关键字带反引号-合理报错
drop synonym if exists `blob`;
drop table if exists blob_test;