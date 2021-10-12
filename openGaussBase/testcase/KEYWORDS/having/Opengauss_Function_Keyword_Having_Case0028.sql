-- @testpoint: opengauss关键字having(保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists having_test;
create table having_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists having;
create synonym having for having_test;

--关键字带双引号-成功
drop synonym if exists "having";
create synonym "having" for having_test;
insert into "having" values (1,'ada'),(2, 'bob');
update "having" set "having".name='cici' where "having".id=2;
select * from "having";

--清理环境
drop synonym "having";

--关键字带单引号-合理报错
drop synonym if exists 'having';
create synonym 'having' for having_test;
insert into 'having' values (1,'ada'),(2, 'bob');
update 'having' set 'having'.name='cici' where 'having'.id=2;
select * from 'having';

--关键字带反引号-合理报错
drop synonym if exists `having`;
create synonym `having` for having_test;
insert into `having` values (1,'ada'),(2, 'bob');
update `having` set `having`.name='cici' where `having`.id=2;
select * from `having`;

--清理环境
drop table if exists having_test;