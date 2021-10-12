-- @testpoint: opengauss关键字duplicate(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists duplicate_test;
create table duplicate_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists duplicate;
create synonym duplicate for duplicate_test;
insert into duplicate values (1,'ada'),(2, 'bob');
update duplicate set duplicate.name='cici' where duplicate.id=2;
select * from duplicate;
drop synonym if exists duplicate;

--关键字带双引号-成功
drop synonym if exists "duplicate";
create synonym "duplicate" for duplicate_test;
drop synonym if exists "duplicate";

--关键字带单引号-合理报错
drop synonym if exists 'duplicate';
create synonym 'duplicate' for duplicate_test;
insert into 'duplicate' values (1,'ada'),(2, 'bob');
update 'duplicate' set 'duplicate'.name='cici' where 'duplicate'.id=2;
select * from 'duplicate';

--关键字带反引号-合理报错
drop synonym if exists `duplicate`;
create synonym `duplicate` for duplicate_test;
insert into `duplicate` values (1,'ada'),(2, 'bob');
update `duplicate` set `duplicate`.name='cici' where `duplicate`.id=2;
select * from `duplicate`;
drop table if exists duplicate_test;