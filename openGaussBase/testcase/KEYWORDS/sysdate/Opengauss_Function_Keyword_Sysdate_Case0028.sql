-- @testpoint: opengauss关键字sysdate(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists sysdate_test;
create table sysdate_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists sysdate;
create synonym sysdate for sysdate_test;


--关键字带双引号-成功
drop synonym if exists "sysdate";
create synonym "sysdate" for sysdate_test;
insert into "sysdate" values (1,'ada'),(2, 'bob');
update "sysdate" set "sysdate".name='cici' where "sysdate".id=2;
select * from "sysdate";
drop synonym "sysdate";
--关键字带单引号-合理报错
drop synonym if exists 'sysdate';
create synonym 'sysdate' for sysdate_test;
insert into 'sysdate' values (1,'ada'),(2, 'bob');
update 'sysdate' set 'sysdate'.name='cici' where 'sysdate'.id=2;
select * from 'sysdate';

--关键字带反引号-合理报错
drop synonym if exists `sysdate`;
create synonym `sysdate` for sysdate_test;
insert into `sysdate` values (1,'ada'),(2, 'bob');
update `sysdate` set `sysdate`.name='cici' where `sysdate`.id=2;
select * from `sysdate`;

--清理环境
drop table if exists sysdate_test;