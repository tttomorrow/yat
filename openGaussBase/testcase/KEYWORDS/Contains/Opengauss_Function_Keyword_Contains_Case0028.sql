-- @testpoint: opengauss关键字contains(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists contains_test;
create table contains_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists contains;
create synonym contains for contains_test;
insert into contains values (1,'ada'),(2, 'bob');
update contains set contains.name='cici' where contains.id=2;
select * from contains;
drop synonym if exists contains;

--关键字带双引号-成功
drop synonym if exists "contains";
create synonym "contains" for contains_test;
drop synonym if exists "contains";

--关键字带单引号-合理报错
drop synonym if exists 'contains';
create synonym 'contains' for contains_test;
insert into 'contains' values (1,'ada'),(2, 'bob');
update 'contains' set 'contains'.name='cici' where 'contains'.id=2;
select * from 'contains';

--关键字带反引号-合理报错
drop synonym if exists `contains`;
create synonym `contains` for contains_test;
insert into `contains` values (1,'ada'),(2, 'bob');
update `contains` set `contains`.name='cici' where `contains`.id=2;
select * from `contains`;

--清理环境
drop table if exists contains_test;