-- @testpoint: opengauss关键字not(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists not_test;
create table not_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists not;
create synonym not for not_test;


--关键字带双引号-成功
drop synonym if exists "not";
create synonym "not" for not_test;
insert into "not" values (1,'ada'),(2, 'bob');
update "not" set "not".name='cici' where "not".id=2;
select * from "not";

--清理环境
drop synonym "not";

--关键字带单引号-合理报错
drop synonym if exists 'not';
create synonym 'not' for not_test;
insert into 'not' values (1,'ada'),(2, 'bob');
update 'not' set 'not'.name='cici' where 'not'.id=2;
select * from 'not';

--关键字带反引号-合理报错
drop synonym if exists `not`;
create synonym `not` for not_test;
insert into `not` values (1,'ada'),(2, 'bob');
update `not` set `not`.name='cici' where `not`.id=2;
select * from `not`;
--清理环境
drop synonym if exists "not";
drop table if exists not_test;