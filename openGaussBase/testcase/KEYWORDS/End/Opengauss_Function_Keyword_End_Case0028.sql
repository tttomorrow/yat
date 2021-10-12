-- @testpoint: opengauss关键字end(保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists end_test;
create table end_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists end;
create synonym end for end_test;


--关键字带双引号-成功
drop synonym if exists "end";
create synonym "end" for end_test;
insert into "end" values (1,'ada'),(2, 'bob');
update "end" set "end".name='cici' where "end".id=2;
select * from "end";
drop synonym "end";
--关键字带单引号-合理报错
drop synonym if exists 'end';
create synonym 'end' for end_test;
insert into 'end' values (1,'ada'),(2, 'bob');
update 'end' set 'end'.name='cici' where 'end'.id=2;
select * from 'end';

--关键字带反引号-合理报错
drop synonym if exists `end`;
create synonym `end` for end_test;
insert into `end` values (1,'ada'),(2, 'bob');
update `end` set `end`.name='cici' where `end`.id=2;
select * from `end`;
drop table if exists end_test;