-- @testpoint: opengauss关键字ada(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists ada_test;
create table ada_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists ada;
create synonym ada for ada_test;
insert into ada values (1,'ada'),(2, 'bob');
update ada set ada.name='cici' where ada.id=2;
select * from ada;

--清理环境
drop synonym if exists ada;

--关键字带双引号-成功
drop synonym if exists "ada";
create synonym "ada" for ada_test;
insert into "ada" values (1,'ada'),(2, 'bob');
update "ada" set "ada".name='cici' where "ada".id=2;
select * from "ada";

--清理环境
drop synonym if exists "ada";
drop table if exists ada_test;

--关键字带单引号-合理报错
drop synonym if exists 'ada';

--关键字带反引号-合理报错
drop synonym if exists `ada`;
