-- @testpoint: opengauss关键字outer(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists outer_test;
create table outer_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists outer;
create synonym outer for outer_test;


--关键字带双引号-成功
drop synonym if exists "outer";
create synonym "outer" for outer_test;
insert into "outer" values (1,'ada'),(2, 'bob');
update "outer" set "outer".name='cici' where "outer".id=2;
select * from "outer";

--清理环境
drop synonym "outer";

--关键字带单引号-合理报错
drop synonym if exists 'outer';
create synonym 'outer' for outer_test;
insert into 'outer' values (1,'ada'),(2, 'bob');
update 'outer' set 'outer'.name='cici' where 'outer'.id=2;
select * from 'outer';

--关键字带反引号-合理报错
drop synonym if exists `outer`;
create synonym `outer` for outer_test;
insert into `outer` values (1,'ada'),(2, 'bob');
update `outer` set `outer`.name='cici' where `outer`.id=2;
select * from `outer`;
--清理环境
drop table if exists outer_test cascade;