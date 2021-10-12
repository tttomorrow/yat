-- @testpoint: opengauss关键字rollup(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists rollup_test;
create table rollup_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists rollup;
create synonym rollup for rollup_test;
insert into rollup values (1,'ada'),(2, 'bob');
update rollup set rollup.name='cici' where rollup.id=2;
select * from rollup;

--清理环境
drop synonym if exists rollup;

--关键字带双引号-成功
drop synonym if exists "rollup";
create synonym "rollup" for rollup_test;
insert into "rollup" values (1,'ada'),(2, 'bob');
update "rollup" set "rollup".name='cici' where "rollup".id=2;
select * from "rollup";

--清理环境
drop synonym if exists "rollup";

--关键字带单引号-合理报错
drop synonym if exists 'rollup';

--关键字带反引号-合理报错
drop synonym if exists `rollup`;
drop table if exists rollup_test;