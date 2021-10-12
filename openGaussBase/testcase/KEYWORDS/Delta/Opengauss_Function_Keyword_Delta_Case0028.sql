-- @testpoint: opengauss关键字delta(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists delta_test;
create table delta_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists delta;
create synonym delta for delta_test;
insert into delta values (1,'ada'),(2, 'bob');
update delta set delta.name='cici' where delta.id=2;
select * from delta;
drop synonym if exists delta;

--关键字带双引号-成功
drop synonym if exists "delta";
create synonym "delta" for delta_test;
drop synonym if exists "delta";

--关键字带单引号-合理报错
drop synonym if exists 'delta';
create synonym 'delta' for delta_test;
insert into 'delta' values (1,'ada'),(2, 'bob');
update 'delta' set 'delta'.name='cici' where 'delta'.id=2;
select * from 'delta';

--关键字带反引号-合理报错
drop synonym if exists `delta`;
create synonym `delta` for delta_test;
insert into `delta` values (1,'ada'),(2, 'bob');
update `delta` set `delta`.name='cici' where `delta`.id=2;
select * from `delta`;
drop table if exists delta_test;