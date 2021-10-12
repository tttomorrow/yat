-- @testpoint: opengauss关键字cluster(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists cluster_test;
create table cluster_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists cluster;
create synonym cluster for cluster_test;
insert into cluster values (1,'ada'),(2, 'bob');
update cluster set cluster.name='cici' where cluster.id=2;
select * from cluster;

--清理环境
drop synonym if exists cluster;

--关键字带双引号-成功
drop synonym if exists "cluster";
create synonym "cluster" for cluster_test;
insert into "cluster" values (1,'ada'),(2, 'bob');
update "cluster" set "cluster".name='cici' where "cluster".id=2;
select * from "cluster";

--清理环境
drop synonym if exists "cluster";

--关键字带单引号-合理报错
drop synonym if exists 'cluster';

--关键字带反引号-合理报错
drop synonym if exists `cluster`;
drop table if exists cluster_test;