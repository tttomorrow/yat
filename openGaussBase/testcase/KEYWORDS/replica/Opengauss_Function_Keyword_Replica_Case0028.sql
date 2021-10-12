-- @testpoint: opengauss关键字replica(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists replica_test;
create table replica_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists replica;
create synonym replica for replica_test;
insert into replica values (1,'ada'),(2, 'bob');
update replica set replica.name='cici' where replica.id=2;
select * from replica;
drop synonym if exists replica;

--关键字带双引号-成功
drop synonym if exists "replica";
create synonym "replica" for replica_test;
insert into "replica" values (1,'ada'),(2, 'bob');
update "replica" set "replica".name='cici' where "replica".id=2;
select * from "replica";
drop synonym if exists "replica";

--关键字带单引号-合理报错
drop synonym if exists 'replica';

--关键字带反引号-合理报错
drop synonym if exists `replica`;
drop table if exists replica_test;