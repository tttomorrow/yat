-- @testpoint: opengauss关键字distinct(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists distinct_test;
create table distinct_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists distinct;
create synonym distinct for distinct_test;


--关键字带双引号-成功
drop synonym if exists "distinct";
create synonym "distinct" for distinct_test;
insert into "distinct" values (1,'ada'),(2, 'bob');
update "distinct" set "distinct".name='cici' where "distinct".id=2;
select * from "distinct";
drop synonym "distinct";
--关键字带单引号-合理报错
drop synonym if exists 'distinct';
create synonym 'distinct' for distinct_test;
insert into 'distinct' values (1,'ada'),(2, 'bob');
update 'distinct' set 'distinct'.name='cici' where 'distinct'.id=2;
select * from 'distinct';

--关键字带反引号-合理报错
drop synonym if exists `distinct`;
create synonym `distinct` for distinct_test;
insert into `distinct` values (1,'ada'),(2, 'bob');
update `distinct` set `distinct`.name='cici' where `distinct`.id=2;
select * from `distinct`;
drop table if exists distinct_test;