-- @testpoint: opengauss关键字trailing(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists trailing_test;
create table trailing_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists trailing;
create synonym trailing for trailing_test;


--关键字带双引号-成功
drop synonym if exists "trailing";
create synonym "trailing" for trailing_test;
insert into "trailing" values (1,'ada'),(2, 'bob');
update "trailing" set "trailing".name='cici' where "trailing".id=2;
select * from "trailing";
drop synonym "trailing";
--关键字带单引号-合理报错
drop synonym if exists 'trailing';
create synonym 'trailing' for trailing_test;
insert into 'trailing' values (1,'ada'),(2, 'bob');
update 'trailing' set 'trailing'.name='cici' where 'trailing'.id=2;
select * from 'trailing';

--关键字带反引号-合理报错
drop synonym if exists `trailing`;
create synonym `trailing` for trailing_test;
insert into `trailing` values (1,'ada'),(2, 'bob');
update `trailing` set `trailing`.name='cici' where `trailing`.id=2;
select * from `trailing`;

--清理环境
drop table if exists trailing_test;