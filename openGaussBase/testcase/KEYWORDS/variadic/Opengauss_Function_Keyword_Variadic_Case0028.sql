-- @testpoint: opengauss关键字variadic(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists variadic_test;
create table variadic_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists variadic;
create synonym variadic for variadic_test;


--关键字带双引号-成功
drop synonym if exists "variadic";
create synonym "variadic" for variadic_test;
insert into "variadic" values (1,'ada'),(2, 'bob');
update "variadic" set "variadic".name='cici' where "variadic".id=2;
select * from "variadic";

--清理环境
drop synonym "variadic";

--关键字带单引号-合理报错
drop synonym if exists 'variadic';
create synonym 'variadic' for variadic_test;
insert into 'variadic' values (1,'ada'),(2, 'bob');
update 'variadic' set 'variadic'.name='cici' where 'variadic'.id=2;
select * from 'variadic';

--关键字带反引号-合理报错
drop synonym if exists `variadic`;
create synonym `variadic` for variadic_test;
insert into `variadic` values (1,'ada'),(2, 'bob');
update `variadic` set `variadic`.name='cici' where `variadic`.id=2;
select * from `variadic`;
drop table if exists variadic_test;