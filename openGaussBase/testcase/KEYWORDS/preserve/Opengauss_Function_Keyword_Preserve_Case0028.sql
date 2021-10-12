-- @testpoint: opengauss关键字preserve(非保留)，作为同义词对象名,合理报错


--前置条件
drop table if exists preserve_test;
create table preserve_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists preserve;
create synonym preserve for preserve_test;
insert into preserve values (1,'ada'),(2, 'bob');
update preserve set preserve.name='cici' where preserve.id=2;
select * from preserve;

--关键字带双引号-成功
drop synonym if exists "preserve";
create synonym "preserve" for preserve_test;
insert into "preserve" values (1,'ada'),(2, 'bob');
update "preserve" set "preserve".name='cici' where "preserve".id=2;
select * from "preserve";

--关键字带单引号-合理报错
drop synonym if exists 'preserve';
create synonym 'preserve' for preserve_test;

--关键字带反引号-合理报错
drop synonym if exists `preserve`;
create synonym `preserve` for preserve_test;

--清理环境
drop synonym if exists preserve;
drop synonym if exists "preserve";
drop table if exists preserve_test;
