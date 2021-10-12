-- @testpoint: opengauss关键字restrict(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists restrict_test;
create table restrict_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists restrict;
create synonym restrict for restrict_test;
insert into restrict values (1,'ada'),(2, 'bob');
update restrict set restrict.name='cici' where restrict.id=2;
select * from restrict;
drop synonym if exists restrict;

--关键字带双引号-成功
drop synonym if exists "restrict";
create synonym "restrict" for restrict_test;
insert into "restrict" values (1,'ada'),(2, 'bob');
update "restrict" set "restrict".name='cici' where "restrict".id=2;
select * from "restrict";
drop synonym if exists "restrict";

--关键字带单引号-合理报错
drop synonym if exists 'restrict';

--关键字带反引号-合理报错
drop synonym if exists `restrict`;
drop table if exists restrict_test;