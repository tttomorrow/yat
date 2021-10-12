-- @testpoint: opengauss关键字do(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists do_test;
create table do_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists do;
create synonym do for do_test;


--关键字带双引号-成功
drop synonym if exists "do";
create synonym "do" for do_test;
insert into "do" values (1,'ada'),(2, 'bob');
update "do" set "do".name='cici' where "do".id=2;
select * from "do";
drop synonym "do";
--关键字带单引号-合理报错
drop synonym if exists 'do';
create synonym 'do' for do_test;
insert into 'do' values (1,'ada'),(2, 'bob');
update 'do' set 'do'.name='cici' where 'do'.id=2;
select * from 'do';

--关键字带反引号-合理报错
drop synonym if exists `do`;
create synonym `do` for do_test;
insert into `do` values (1,'ada'),(2, 'bob');
update `do` set `do`.name='cici' where `do`.id=2;
select * from `do`;
drop table if exists do_test;