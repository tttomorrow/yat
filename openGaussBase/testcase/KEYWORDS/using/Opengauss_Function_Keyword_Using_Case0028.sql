-- @testpoint: opengauss关键字using(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists using_test;
create table using_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists using;
create synonym using for using_test;


--关键字带双引号-成功
drop synonym if exists "using";
create synonym "using" for using_test;
insert into "using" values (1,'ada'),(2, 'bob');
update "using" set "using".name='cici' where "using".id=2;
select * from "using";

--清理环境
drop synonym "using";

--关键字带单引号-合理报错
drop synonym if exists 'using';
create synonym 'using' for using_test;
insert into 'using' values (1,'ada'),(2, 'bob');
update 'using' set 'using'.name='cici' where 'using'.id=2;
select * from 'using';

--关键字带反引号-合理报错
drop synonym if exists `using`;
create synonym `using` for using_test;
insert into `using` values (1,'ada'),(2, 'bob');
update `using` set `using`.name='cici' where `using`.id=2;
select * from `using`;
drop table if exists using_test;