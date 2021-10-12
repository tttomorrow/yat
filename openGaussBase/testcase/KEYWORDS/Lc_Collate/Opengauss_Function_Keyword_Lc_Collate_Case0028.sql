-- @testpoint: opengauss关键字Lc_Collate(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists Lc_Collate;
create synonym Lc_Collate for explain_test;
insert into Lc_Collate values (1,'ada'),(2, 'bob');
update Lc_Collate set Lc_Collate.name='cici' where Lc_Collate.id=2;
select * from Lc_Collate;

--关键字带双引号-成功
drop synonym if exists "Lc_Collate";
create synonym "Lc_Collate" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'Lc_Collate';
create synonym 'Lc_Collate' for explain_test;
insert into 'Lc_Collate' values (1,'ada'),(2, 'bob');
update 'Lc_Collate' set 'Lc_Collate'.name='cici' where 'Lc_Collate'.id=2;
select * from 'Lc_Collate';

--关键字带反引号-合理报错
drop synonym if exists `Lc_Collate`;
create synonym `Lc_Collate` for explain_test;
insert into `Lc_Collate` values (1,'ada'),(2, 'bob');
update `Lc_Collate` set `Lc_Collate`.name='cici' where `Lc_Collate`.id=2;
select * from `Lc_Collate`;
--清理环境
drop synonym if exists lc_Collate;
drop synonym if exists "Lc_Collate";
drop table if exists explain_test;