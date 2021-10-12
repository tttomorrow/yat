-- @testpoint: opengauss关键字collate(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists collate_test;
create table collate_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists collate;
create synonym collate for collate_test;


--关键字带双引号-成功
drop synonym if exists "collate";
create synonym "collate" for collate_test;
insert into "collate" values (1,'ada'),(2, 'bob');
update "collate" set "collate".name='cici' where "collate".id=2;
select * from "collate";
drop synonym "collate";
--关键字带单引号-合理报错
drop synonym if exists 'collate';
create synonym 'collate' for collate_test;
insert into 'collate' values (1,'ada'),(2, 'bob');
update 'collate' set 'collate'.name='cici' where 'collate'.id=2;
select * from 'collate';

--关键字带反引号-合理报错
drop synonym if exists `collate`;
create synonym `collate` for collate_test;
insert into `collate` values (1,'ada'),(2, 'bob');
update `collate` set `collate`.name='cici' where `collate`.id=2;
select * from `collate`;
drop table if exists collate_test;