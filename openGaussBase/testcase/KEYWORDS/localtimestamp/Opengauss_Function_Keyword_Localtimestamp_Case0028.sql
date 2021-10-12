-- @testpoint: opengauss关键字localtimestamp(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists localtimestamp_test;
create table localtimestamp_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists localtimestamp;
create synonym localtimestamp for localtimestamp_test;


--关键字带双引号-成功
drop synonym if exists "localtimestamp";
create synonym "localtimestamp" for localtimestamp_test;
insert into "localtimestamp" values (1,'ada'),(2, 'bob');
update "localtimestamp" set "localtimestamp".name='cici' where "localtimestamp".id=2;
select * from "localtimestamp";

--清理环境
drop synonym "localtimestamp";

--关键字带单引号-合理报错
drop synonym if exists 'localtimestamp';
create synonym 'localtimestamp' for localtimestamp_test;
insert into 'localtimestamp' values (1,'ada'),(2, 'bob');
update 'localtimestamp' set 'localtimestamp'.name='cici' where 'localtimestamp'.id=2;
select * from 'localtimestamp';

--关键字带反引号-合理报错
drop synonym if exists `localtimestamp`;
create synonym `localtimestamp` for localtimestamp_test;
insert into `localtimestamp` values (1,'ada'),(2, 'bob');
update `localtimestamp` set `localtimestamp`.name='cici' where `localtimestamp`.id=2;
select * from `localtimestamp`;
--清理环境
drop table if exists localtimestamp_test cascade;