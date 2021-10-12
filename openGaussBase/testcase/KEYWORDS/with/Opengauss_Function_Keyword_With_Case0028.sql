-- @testpoint: opengauss关键字with(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists with_test;
create table with_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists with;
create synonym with for with_test;


--关键字带双引号-成功
drop synonym if exists "with";
create synonym "with" for with_test;
insert into "with" values (1,'ada'),(2, 'bob');
update "with" set "with".name='cici' where "with".id=2;
select * from "with";

--清理环境
drop synonym "with";

--关键字带单引号-合理报错
drop synonym if exists 'with';
create synonym 'with' for with_test;
insert into 'with' values (1,'ada'),(2, 'bob');
update 'with' set 'with'.name='cici' where 'with'.id=2;
select * from 'with';

--关键字带反引号-合理报错
drop synonym if exists `with`;
create synonym `with` for with_test;
insert into `with` values (1,'ada'),(2, 'bob');
update `with` set `with`.name='cici' where `with`.id=2;
select * from `with`;
drop table if exists with_test;