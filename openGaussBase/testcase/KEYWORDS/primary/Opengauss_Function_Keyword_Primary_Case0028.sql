-- @testpoint: opengauss关键字primary(保留)，作为同义词对象名,合理报错


--前置条件
drop table if exists primary_test;
create table primary_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists primary;
create synonym primary for primary_test;


--关键字带双引号-成功
drop synonym if exists "primary";
create synonym "primary" for primary_test;
insert into "primary" values (1,'ada'),(2, 'bob');
update "primary" set "primary".name='cici' where "primary".id=2;
select * from "primary";

--清理环境
drop synonym "primary";

--关键字带单引号-合理报错
drop synonym if exists 'primary';
create synonym 'primary' for primary_test;
insert into 'primary' values (1,'ada'),(2, 'bob');
update 'primary' set 'primary'.name='cici' where 'primary'.id=2;
select * from 'primary';

--关键字带反引号-合理报错
drop synonym if exists `primary`;
create synonym `primary` for primary_test;
insert into `primary` values (1,'ada'),(2, 'bob');
update `primary` set `primary`.name='cici' where `primary`.id=2;
select * from `primary`;

--清理环境
drop table if exists primary_test;