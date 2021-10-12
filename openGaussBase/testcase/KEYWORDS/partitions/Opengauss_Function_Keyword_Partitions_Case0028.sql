-- @testpoint: opengauss关键字partitions(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists partitions_test;
create table partitions_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists partitions;
create synonym partitions for partitions_test;
insert into partitions values (1,'ada'),(2, 'bob');
update partitions set partitions.name='cici' where partitions.id=2;
select * from partitions;

--关键字带双引号-成功
drop synonym if exists "partitions";
create synonym "partitions" for partitions_test;


--关键字带单引号-合理报错
drop synonym if exists 'partitions';
create synonym 'partitions' for partitions_test;
insert into 'partitions' values (1,'ada'),(2, 'bob');
update 'partitions' set 'partitions'.name='cici' where 'partitions'.id=2;
select * from 'partitions';

--关键字带反引号-合理报错
drop synonym if exists `partitions`;
create synonym `partitions` for partitions_test;
insert into `partitions` values (1,'ada'),(2, 'bob');
update `partitions` set `partitions`.name='cici' where `partitions`.id=2;
select * from `partitions`;
--清理环境
drop synonym if exists "partitions";
drop synonym if exists partitions;
drop table if exists partitions_test;