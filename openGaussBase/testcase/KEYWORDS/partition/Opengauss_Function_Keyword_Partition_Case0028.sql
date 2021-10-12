-- @testpoint: opengauss关键字partition(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists partition_test;
create table partition_test(id int,name varchar(10));

--关键字不带引号-合理报错
drop synonym if exists partition;
create synonym partition for partition_test;
insert into partition values (1,'ada'),(2, 'bob');
update partition set partition.name='cici' where partition.id=2;
select * from partition;

--关键字带双引号-成功
drop synonym if exists "partition";
create synonym "partition" for partition_test;


--关键字带单引号-合理报错
drop synonym if exists 'partition';
create synonym 'partition' for partition_test;
insert into 'partition' values (1,'ada'),(2, 'bob');
update 'partition' set 'partition'.name='cici' where 'partition'.id=2;
select * from 'partition';

--关键字带反引号-合理报错
drop synonym if exists `partition`;
create synonym `partition` for partition_test;
insert into `partition` values (1,'ada'),(2, 'bob');
update `partition` set `partition`.name='cici' where `partition`.id=2;
select * from `partition`;
--清理环境
drop synonym if exists "partition";
drop table if exists partition_test;