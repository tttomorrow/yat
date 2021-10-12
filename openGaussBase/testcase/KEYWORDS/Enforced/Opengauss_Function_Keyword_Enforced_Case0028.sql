-- @testpoint: opengauss关键字enforced(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists enforced_test;
create table enforced_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists enforced;
create synonym enforced for enforced_test;
insert into enforced values (1,'ada'),(2, 'bob');
update enforced set enforced.name='cici' where enforced.id=2;
select * from enforced;
drop synonym if exists enforced;

--关键字带双引号-成功
drop synonym if exists "enforced";
create synonym "enforced" for enforced_test;
drop synonym if exists "enforced";

--关键字带单引号-合理报错
drop synonym if exists 'enforced';
create synonym 'enforced' for enforced_test;
insert into 'enforced' values (1,'ada'),(2, 'bob');
update 'enforced' set 'enforced'.name='cici' where 'enforced'.id=2;
select * from 'enforced';

--关键字带反引号-合理报错
drop synonym if exists `enforced`;
create synonym `enforced` for enforced_test;
insert into `enforced` values (1,'ada'),(2, 'bob');
update `enforced` set `enforced`.name='cici' where `enforced`.id=2;
select * from `enforced`;
drop table if exists enforced_test;