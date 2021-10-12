-- @testpoint: opengauss关键字on(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists on_test;
create table on_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists on;
create synonym on for on_test;


--关键字带双引号-成功
drop synonym if exists "on";
create synonym "on" for on_test;
insert into "on" values (1,'ada'),(2, 'bob');
update "on" set "on".name='cici' where "on".id=2;
select * from "on";

--清理环境
drop synonym "on";

--关键字带单引号-合理报错
drop synonym if exists 'on';
create synonym 'on' for on_test;
insert into 'on' values (1,'ada'),(2, 'bob');
update 'on' set 'on'.name='cici' where 'on'.id=2;
select * from 'on';

--关键字带反引号-合理报错
drop synonym if exists `on`;
create synonym `on` for on_test;
insert into `on` values (1,'ada'),(2, 'bob');
update `on` set `on`.name='cici' where `on`.id=2;
select * from `on`;
--清理环境
drop table if exists on_test cascade;