-- @testpoint: opengauss关键字group(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists group_test;
create table group_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists group;
create synonym group for group_test;


--关键字带双引号-成功
drop synonym if exists "group";
create synonym "group" for group_test;
insert into "group" values (1,'ada'),(2, 'bob');
update "group" set "group".name='cici' where "group".id=2;
select * from "group";

--清理环境
drop synonym "group";

--关键字带单引号-合理报错
drop synonym if exists 'group';
create synonym 'group' for group_test;
insert into 'group' values (1,'ada'),(2, 'bob');
update 'group' set 'group'.name='cici' where 'group'.id=2;
select * from 'group';

--关键字带反引号-合理报错
drop synonym if exists `group`;
create synonym `group` for group_test;
insert into `group` values (1,'ada'),(2, 'bob');
update `group` set `group`.name='cici' where `group`.id=2;
select * from `group`;

--清理环境
drop table if exists group_test;