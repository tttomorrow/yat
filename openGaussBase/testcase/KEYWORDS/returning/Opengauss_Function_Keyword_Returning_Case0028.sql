-- @testpoint: opengauss关键字returning(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists returning_test;
create table returning_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists returning;
create synonym returning for returning_test;


--关键字带双引号-成功
drop synonym if exists "returning";
create synonym "returning" for returning_test;
insert into "returning" values (1,'ada'),(2, 'bob');
update "returning" set "returning".name='cici' where "returning".id=2;
select * from "returning";

--清理环境
drop synonym "returning";

--关键字带单引号-合理报错
drop synonym if exists 'returning';
create synonym 'returning' for returning_test;
insert into 'returning' values (1,'ada'),(2, 'bob');
update 'returning' set 'returning'.name='cici' where 'returning'.id=2;
select * from 'returning';

--关键字带反引号-合理报错
drop synonym if exists `returning`;
create synonym `returning` for returning_test;
insert into `returning` values (1,'ada'),(2, 'bob');
update `returning` set `returning`.name='cici' where `returning`.id=2;
select * from `returning`;
drop table if exists returning_test;