-- @testpoint: opengauss关键字recursive(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists recursive_test;
create table recursive_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists recursive;
create synonym recursive for recursive_test;
insert into recursive values (1,'ada'),(2, 'bob');
update recursive set recursive.name='cici' where recursive.id=2;
select * from recursive;
drop synonym if exists recursive;

--关键字带双引号-成功
drop synonym if exists "recursive";
create synonym "recursive" for recursive_test;
insert into "recursive" values (1,'ada'),(2, 'bob');
update "recursive" set "recursive".name='cici' where "recursive".id=2;
select * from "recursive";
drop synonym if exists "recursive";

--关键字带单引号-合理报错
drop synonym if exists 'recursive';

--关键字带反引号-合理报错
drop synonym if exists `recursive`;
drop table if exists recursive_test;