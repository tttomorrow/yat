-- @testpoint: opengauss关键字notnull(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists notnull_test;
create table notnull_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists notnull;
create synonym notnull for notnull_test;


--关键字带双引号-成功
drop synonym if exists "notnull";
create synonym "notnull" for notnull_test;
insert into "notnull" values (1,'ada'),(2, 'bob');
update "notnull" set "notnull".name='cici' where "notnull".id=2;
select * from "notnull";

--清理环境
drop synonym "notnull";

--关键字带单引号-合理报错
drop synonym if exists 'notnull';
create synonym 'notnull' for notnull_test;
insert into 'notnull' values (1,'ada'),(2, 'bob');
update 'notnull' set 'notnull'.name='cici' where 'notnull'.id=2;
select * from 'notnull';

--关键字带反引号-合理报错
drop synonym if exists `notnull`;
create synonym `notnull` for notnull_test;
insert into `notnull` values (1,'ada'),(2, 'bob');
update `notnull` set `notnull`.name='cici' where `notnull`.id=2;
select * from `notnull`;
--清理环境
drop table if exists notnull_test;