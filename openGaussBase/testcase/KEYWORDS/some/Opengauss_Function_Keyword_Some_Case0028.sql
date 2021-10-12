-- @testpoint: opengauss关键字some(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists some_test;
create table some_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists some;
create synonym some for some_test;


--关键字带双引号-成功
drop synonym if exists "some";
create synonym "some" for some_test;
insert into "some" values (1,'ada'),(2, 'bob');
update "some" set "some".name='cici' where "some".id=2;
select * from "some";

--清理环境
drop synonym "some";

--关键字带单引号-合理报错
drop synonym if exists 'some';
create synonym 'some' for some_test;
insert into 'some' values (1,'ada'),(2, 'bob');
update 'some' set 'some'.name='cici' where 'some'.id=2;
select * from 'some';

--关键字带反引号-合理报错
drop synonym if exists `some`;
create synonym `some` for some_test;
insert into `some` values (1,'ada'),(2, 'bob');
update `some` set `some`.name='cici' where `some`.id=2;
select * from `some`;
drop table if exists some_test;