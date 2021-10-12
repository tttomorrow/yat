-- @testpoint: opengauss关键字definer(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists definer_test;
create table definer_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists definer;
create synonym definer for definer_test;
insert into definer values (1,'ada'),(2, 'bob');
update definer set definer.name='cici' where definer.id=2;
select * from definer;
drop synonym if exists definer;

--关键字带双引号-成功
drop synonym if exists "definer";
create synonym "definer" for definer_test;
drop synonym if exists "definer";

--关键字带单引号-合理报错
drop synonym if exists 'definer';
create synonym 'definer' for definer_test;
insert into 'definer' values (1,'ada'),(2, 'bob');
update 'definer' set 'definer'.name='cici' where 'definer'.id=2;
select * from 'definer';

--关键字带反引号-合理报错
drop synonym if exists `definer`;
create synonym `definer` for definer_test;
insert into `definer` values (1,'ada'),(2, 'bob');
update `definer` set `definer`.name='cici' where `definer`.id=2;
select * from `definer`;
drop table if exists definer_test;