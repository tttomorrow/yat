-- @testpoint: opengauss关键字checked(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists checked_test;
create table checked_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists checked;
create synonym checked for checked_test;
insert into checked values (1,'ada'),(2, 'bob');
update checked set checked.name='cici' where checked.id=2;
select * from checked;

--清理环境
drop synonym if exists checked;

--关键字带双引号-成功
drop synonym if exists "checked";
create synonym "checked" for checked_test;
insert into "checked" values (1,'ada'),(2, 'bob');
update "checked" set "checked".name='cici' where "checked".id=2;
select * from "checked";

--清理环境
drop synonym if exists "checked";

--关键字带单引号-合理报错
drop synonym if exists 'checked';

--关键字带反引号-合理报错
drop synonym if exists `checked`;
drop table if exists checked_test;