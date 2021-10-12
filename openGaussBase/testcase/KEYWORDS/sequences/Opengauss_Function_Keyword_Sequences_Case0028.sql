-- @testpoint: opengauss关键字sequences(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists sequences;
create synonym sequences for explain_test;
insert into sequences values (1,'ada'),(2, 'bob');
update sequences set sequences.name='cici' where sequences.id=2;
select * from sequences;
drop synonym if exists sequences;

--关键字带双引号-成功
drop synonym if exists "sequences";
create synonym "sequences" for explain_test;
drop synonym if exists "sequences";

--关键字带单引号-合理报错
drop synonym if exists 'sequences';
create synonym 'sequences' for explain_test;
insert into 'sequences' values (1,'ada'),(2, 'bob');
update 'sequences' set 'sequences'.name='cici' where 'sequences'.id=2;
select * from 'sequences';

--关键字带反引号-合理报错
drop synonym if exists `sequences`;
create synonym `sequences` for explain_test;
insert into `sequences` values (1,'ada'),(2, 'bob');
update `sequences` set `sequences`.name='cici' where `sequences`.id=2;
select * from `sequences`;
drop table if exists explain_test;