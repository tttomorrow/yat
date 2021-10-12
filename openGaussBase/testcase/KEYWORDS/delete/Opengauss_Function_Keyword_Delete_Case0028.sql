-- @testpoint: opengauss关键字delete(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists delete_test;
create table delete_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists delete;
create synonym delete for delete_test;
insert into delete values (1,'ada'),(2, 'bob');
update delete set delete.name='cici' where delete.id=2;
select * from delete;
drop synonym if exists delete;

--关键字带双引号-成功
drop synonym if exists "delete";
create synonym "delete" for delete_test;
drop synonym if exists "delete";

--关键字带单引号-合理报错
drop synonym if exists 'delete';
create synonym 'delete' for delete_test;
insert into 'delete' values (1,'ada'),(2, 'bob');
update 'delete' set 'delete'.name='cici' where 'delete'.id=2;
select * from 'delete';

--关键字带反引号-合理报错
drop synonym if exists `delete`;
create synonym `delete` for delete_test;
insert into `delete` values (1,'ada'),(2, 'bob');
update `delete` set `delete`.name='cici' where `delete`.id=2;
select * from `delete`;
drop table if exists delete_test;
