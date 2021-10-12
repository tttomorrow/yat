-- @testpoint: opengauss关键字result(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists result_test;
create table result_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists result;
create synonym result for result_test;
insert into result values (1,'ada'),(2, 'bob');
update result set result.name='cici' where result.id=2;
select * from result;
drop synonym if exists result;

--关键字带双引号-成功
drop synonym if exists "result";
create synonym "result" for result_test;
insert into "result" values (1,'ada'),(2, 'bob');
update "result" set "result".name='cici' where "result".id=2;
select * from "result";
drop synonym if exists "result";

--关键字带单引号-合理报错
drop synonym if exists 'result';

--关键字带反引号-合理报错
drop synonym if exists `result`;
drop table if exists result_test;