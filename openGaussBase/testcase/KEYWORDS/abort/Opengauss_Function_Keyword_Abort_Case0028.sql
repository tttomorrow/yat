-- @testpoint: opengauss关键字abort(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists abort_test;
create table abort_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists abort;
create synonym abort for abort_test;
insert into abort values (1,'ada'),(2, 'bob');
update abort set abort.name='cici' where abort.id=2;
select * from abort;

--清理环境
drop synonym if exists abort;

--关键字带双引号-成功
drop synonym if exists "abort";
create synonym "abort" for abort_test;
insert into "abort" values (1,'ada'),(2, 'bob');
update "abort" set "abort".name='cici' where "abort".id=2;
select * from "abort";

--清理环境
drop synonym if exists "abort";

--关键字带单引号-合理报错
drop synonym if exists 'abort';

--关键字带反引号-合理报错
drop synonym if exists `abort`;
drop table if exists abort_test;