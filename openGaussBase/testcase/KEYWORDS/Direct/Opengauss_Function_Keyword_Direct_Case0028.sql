-- @testpoint: opengauss关键字direct(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists direct_test;
create table direct_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists direct;
create synonym direct for direct_test;
insert into direct values (1,'ada'),(2, 'bob');
update direct set direct.name='cici' where direct.id=2;
select * from direct;
drop synonym if exists direct;

--关键字带双引号-成功
drop synonym if exists "direct";
create synonym "direct" for direct_test;
drop synonym if exists "direct";

--关键字带单引号-合理报错
drop synonym if exists 'direct';
create synonym 'direct' for direct_test;
insert into 'direct' values (1,'ada'),(2, 'bob');
update 'direct' set 'direct'.name='cici' where 'direct'.id=2;
select * from 'direct';

--关键字带反引号-合理报错
drop synonym if exists `direct`;
create synonym `direct` for direct_test;
insert into `direct` values (1,'ada'),(2, 'bob');
update `direct` set `direct`.name='cici' where `direct`.id=2;
select * from `direct`;
drop table if exists direct_test;