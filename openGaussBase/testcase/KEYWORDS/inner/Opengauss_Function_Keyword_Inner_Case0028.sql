-- @testpoint: opengauss关键字inner(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists inner_test;
create table inner_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists inner;
create synonym inner for inner_test;


--关键字带双引号-成功
drop synonym if exists "inner";
create synonym "inner" for inner_test;
insert into "inner" values (1,'ada'),(2, 'bob');
update "inner" set "inner".name='cici' where "inner".id=2;
select * from "inner";

--清理环境
drop synonym "inner";

--关键字带单引号-合理报错
drop synonym if exists 'inner';
create synonym 'inner' for inner_test;
insert into 'inner' values (1,'ada'),(2, 'bob');
update 'inner' set 'inner'.name='cici' where 'inner'.id=2;
select * from 'inner';

--关键字带反引号-合理报错
drop synonym if exists `inner`;
create synonym `inner` for inner_test;
insert into `inner` values (1,'ada'),(2, 'bob');
update `inner` set `inner`.name='cici' where `inner`.id=2;
select * from `inner`;
--清理环境
drop table if exists inner_test cascade;