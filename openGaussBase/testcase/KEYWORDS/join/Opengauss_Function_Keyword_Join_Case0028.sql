-- @testpoint: opengauss关键字join(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists join_test;
create table join_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists join;
create synonym join for join_test;


--关键字带双引号-成功
drop synonym if exists "join";
create synonym "join" for join_test;
insert into "join" values (1,'ada'),(2, 'bob');
update "join" set "join".name='cici' where "join".id=2;
select * from "join";

--清理环境
drop synonym "join";

--关键字带单引号-合理报错
drop synonym if exists 'join';
create synonym 'join' for join_test;
insert into 'join' values (1,'ada'),(2, 'bob');
update 'join' set 'join'.name='cici' where 'join'.id=2;
select * from 'join';

--关键字带反引号-合理报错
drop synonym if exists `join`;
create synonym `join` for join_test;
insert into `join` values (1,'ada'),(2, 'bob');
update `join` set `join`.name='cici' where `join`.id=2;
select * from `join`;
--清理环境
drop table if exists join_test cascade;