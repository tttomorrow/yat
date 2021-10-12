-- @testpoint: opengauss关键字characteristics(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists characteristics_test;
create table characteristics_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists characteristics;
create synonym characteristics for characteristics_test;
insert into characteristics values (1,'ada'),(2, 'bob');
update characteristics set characteristics.name='cici' where characteristics.id=2;
select * from characteristics;

--清理环境
drop synonym if exists characteristics;

--关键字带双引号-成功
drop synonym if exists "characteristics";
create synonym "characteristics" for characteristics_test;
insert into "characteristics" values (1,'ada'),(2, 'bob');
update "characteristics" set "characteristics".name='cici' where "characteristics".id=2;
select * from "characteristics";

--清理环境
drop synonym if exists "characteristics";

--关键字带单引号-合理报错
drop synonym if exists 'characteristics';

--关键字带反引号-合理报错
drop synonym if exists `characteristics`;
drop table if exists characteristics_test;