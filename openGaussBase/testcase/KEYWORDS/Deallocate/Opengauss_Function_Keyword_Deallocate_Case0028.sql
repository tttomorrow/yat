-- @testpoint: opengauss关键字deallocate(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists deallocate_test;
create table deallocate_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists deallocate;
create synonym deallocate for deallocate_test;
insert into deallocate values (1,'ada'),(2, 'bob');
update deallocate set deallocate.name='cici' where deallocate.id=2;
select * from deallocate;
drop synonym if exists deallocate;

--关键字带双引号-成功
drop synonym if exists "deallocate";
create synonym "deallocate" for deallocate_test;
drop synonym if exists "deallocate";

--关键字带单引号-合理报错
drop synonym if exists 'deallocate';
create synonym 'deallocate' for deallocate_test;
insert into 'deallocate' values (1,'ada'),(2, 'bob');
update 'deallocate' set 'deallocate'.name='cici' where 'deallocate'.id=2;
select * from 'deallocate';

--关键字带反引号-合理报错
drop synonym if exists `deallocate`;
create synonym `deallocate` for deallocate_test;
insert into `deallocate` values (1,'ada'),(2, 'bob');
update `deallocate` set `deallocate`.name='cici' where `deallocate`.id=2;
select * from `deallocate`;
drop table if exists deallocate_test;