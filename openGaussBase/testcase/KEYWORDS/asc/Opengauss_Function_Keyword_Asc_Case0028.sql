-- @testpoint: opengauss关键字Asc(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists Asc_test;
create table Asc_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists Asc;
create synonym Asc for Asc_test;


--关键字带双引号-成功
drop synonym if exists "Asc";
create synonym "Asc" for Asc_test;
insert into "Asc" values (1,'ada'),(2, 'bob');
update "Asc" set "Asc".name='cici' where "Asc".id=2;
select * from "Asc";

--清理环境
drop synonym "Asc";

--关键字带单引号-合理报错
drop synonym if exists 'Asc';
create synonym 'Asc' for Asc_test;
insert into 'Asc' values (1,'ada'),(2, 'bob');
update 'Asc' set 'Asc'.name='cici' where 'Asc'.id=2;
select * from 'Asc';

--关键字带反引号-合理报错
drop synonym if exists `Asc`;
create synonym `Asc` for Asc_test;
insert into `Asc` values (1,'ada'),(2, 'bob');
update `Asc` set `Asc`.name='cici' where `Asc`.id=2;
select * from `Asc`;
drop table if exists Asc_test;