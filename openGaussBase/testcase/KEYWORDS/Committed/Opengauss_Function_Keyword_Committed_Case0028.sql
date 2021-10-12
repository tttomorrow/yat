-- @testpoint: opengauss关键字committed(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists committed_test;
create table committed_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists committed;
create synonym committed for committed_test;
insert into committed values (1,'ada'),(2, 'bob');
update committed set committed.name='cici' where committed.id=2;
select * from committed;
drop synonym if exists committed;
--关键字带双引号-成功
drop synonym if exists "committed";
create synonym "committed" for committed_test;
drop synonym if exists "committed";

--关键字带单引号-合理报错
drop synonym if exists 'committed';
create synonym 'committed' for committed_test;
insert into 'committed' values (1,'ada'),(2, 'bob');
update 'committed' set 'committed'.name='cici' where 'committed'.id=2;
select * from 'committed';

--关键字带反引号-合理报错
drop synonym if exists `committed`;
create synonym `committed` for committed_test;
insert into `committed` values (1,'ada'),(2, 'bob');
update `committed` set `committed`.name='cici' where `committed`.id=2;
select * from `committed`;
drop table if exists committed_test;