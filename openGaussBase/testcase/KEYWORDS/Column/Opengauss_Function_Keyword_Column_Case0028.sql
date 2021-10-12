-- @testpoint: opengauss关键字column(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists column_test;
create table column_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists column;
create synonym column for column_test;


--关键字带双引号-成功
drop synonym if exists "column";
create synonym "column" for column_test;
insert into "column" values (1,'ada'),(2, 'bob');
update "column" set "column".name='cici' where "column".id=2;
select * from "column";
drop synonym "column";
--关键字带单引号-合理报错
drop synonym if exists 'column';
create synonym 'column' for column_test;
insert into 'column' values (1,'ada'),(2, 'bob');
update 'column' set 'column'.name='cici' where 'column'.id=2;
select * from 'column';

--关键字带反引号-合理报错
drop synonym if exists `column`;
create synonym `column` for column_test;
insert into `column` values (1,'ada'),(2, 'bob');
update `column` set `column`.name='cici' where `column`.id=2;
select * from `column`;
drop table if exists column_test;