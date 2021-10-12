-- @testpoint: opengauss关键字modify(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists modify_test;
create table modify_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists modify;
create synonym modify for modify_test;


--关键字带双引号-成功
drop synonym if exists "modify";
create synonym "modify" for modify_test;
insert into "modify" values (1,'ada'),(2, 'bob');
update "modify" set "modify".name='cici' where "modify".id=2;
select * from "modify";

--清理环境
drop synonym "modify";

--关键字带单引号-合理报错
drop synonym if exists 'modify';
create synonym 'modify' for modify_test;
insert into 'modify' values (1,'ada'),(2, 'bob');
update 'modify' set 'modify'.name='cici' where 'modify'.id=2;
select * from 'modify';

--关键字带反引号-合理报错
drop synonym if exists `modify`;
create synonym `modify` for modify_test;
insert into `modify` values (1,'ada'),(2, 'bob');
update `modify` set `modify`.name='cici' where `modify`.id=2;
select * from `modify`;
--清理环境
drop synonym if exists "modify";
drop table if exists modify_test;
