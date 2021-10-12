-- @testpoint: opengauss关键字Date(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号
drop synonym if exists Date;
create synonym Date for explain_test;
insert into Date values (1,'ada'),(2, 'bob');
update Date set Date.name='cici' where Date.id=2;
select * from Date;
drop synonym if exists Date;

--关键字带双引号
drop synonym if exists "Date";
create synonym "Date" for explain_test;
drop synonym if exists "Date";

--关键字带单引号-合理报错
drop synonym if exists 'Date';
create synonym 'Date' for explain_test;
insert into 'Date' values (1,'ada'),(2, 'bob');
update 'Date' set 'Date'.name='cici' where 'Date'.id=2;
select * from 'Date';

--关键字带反引号-合理报错
drop synonym if exists `Date`;
create synonym `Date` for explain_test;
insert into `Date` values (1,'ada'),(2, 'bob');
update `Date` set `Date`.name='cici' where `Date`.id=2;
select * from `Date`;
drop table if exists explain_test;
