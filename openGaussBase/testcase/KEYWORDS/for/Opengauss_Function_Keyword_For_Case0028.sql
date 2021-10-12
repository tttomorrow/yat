-- @testpoint: opengauss关键字for(保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists for_test;
create table for_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists for;
create synonym for for for_test;


--关键字带双引号-成功
drop synonym if exists "for";
create synonym "for" for for_test;
insert into "for" values (1,'ada'),(2, 'bob');
update "for" set "for".name='cici' where "for".id=2;
select * from "for";

--清理环境
drop synonym "for";

--关键字带单引号-合理报错
drop synonym if exists 'for';
create synonym 'for' for for_test;
insert into 'for' values (1,'ada'),(2, 'bob');
update 'for' set 'for'.name='cici' where 'for'.id=2;
select * from 'for';

--关键字带反引号-合理报错
drop synonym if exists `for`;
create synonym `for` for for_test;
insert into `for` values (1,'ada'),(2, 'bob');
update `for` set `for`.name='cici' where `for`.id=2;
select * from `for`;
drop table if exists for_test;