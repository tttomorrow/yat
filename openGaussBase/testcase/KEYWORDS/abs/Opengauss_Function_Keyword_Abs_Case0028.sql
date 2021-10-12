-- @testpoint: opengauss关键字abs(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists abs_test;
create table abs_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists abs;
create synonym abs for abs_test;
insert into abs values (1,'ada'),(2, 'bob');
update abs set abs.name='cici' where abs.id=2;
select * from abs;

--清理环境
drop synonym if exists abs;

--关键字带双引号-成功
drop synonym if exists "abs";
create synonym "abs" for abs_test;
insert into "abs" values (1,'ada'),(2, 'bob');
update "abs" set "abs".name='cici' where "abs".id=2;
select * from "abs";

--清理环境
drop synonym if exists "abs";

--关键字带单引号-合理报错
drop synonym if exists 'abs';

--关键字带反引号-合理报错
drop synonym if exists `abs`;
drop table if exists abs_test;