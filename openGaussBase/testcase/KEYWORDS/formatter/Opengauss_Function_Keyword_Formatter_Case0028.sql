-- @testpoint: opengauss关键字formatter(非保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists formatter;
create synonym formatter for explain_test;
insert into formatter values (1,'ada'),(2, 'bob');
update formatter set formatter.name='cici' where formatter.id=2;
select * from formatter;
drop synonym if exists formatter;

--关键字带双引号-成功
drop synonym if exists "formatter";
create synonym "formatter" for explain_test;
drop synonym if exists "formatter";

--关键字带单引号-合理报错
drop synonym if exists 'formatter';
create synonym 'formatter' for explain_test;
insert into 'formatter' values (1,'ada'),(2, 'bob');
update 'formatter' set 'formatter'.name='cici' where 'formatter'.id=2;
select * from 'formatter';

--关键字带反引号-合理报错
drop synonym if exists `formatter`;
create synonym `formatter` for explain_test;
insert into `formatter` values (1,'ada'),(2, 'bob');
update `formatter` set `formatter`.name='cici' where `formatter`.id=2;
select * from `formatter`;
drop table if exists explain_test;