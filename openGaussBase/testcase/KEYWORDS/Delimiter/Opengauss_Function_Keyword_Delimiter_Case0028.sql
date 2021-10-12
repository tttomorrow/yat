-- @testpoint: opengauss关键字delimiter(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists delimiter_test;
create table delimiter_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists delimiter;
create synonym delimiter for delimiter_test;
insert into delimiter values (1,'ada'),(2, 'bob');
update delimiter set delimiter.name='cici' where delimiter.id=2;
select * from delimiter;
drop synonym if exists delimiter;

--关键字带双引号-成功
drop synonym if exists "delimiter";
create synonym "delimiter" for delimiter_test;
drop synonym if exists "delimiter";

--关键字带单引号-合理报错
drop synonym if exists 'delimiter';
create synonym 'delimiter' for delimiter_test;
insert into 'delimiter' values (1,'ada'),(2, 'bob');
update 'delimiter' set 'delimiter'.name='cici' where 'delimiter'.id=2;
select * from 'delimiter';

--关键字带反引号-合理报错
drop synonym if exists `delimiter`;
create synonym `delimiter` for delimiter_test;
insert into `delimiter` values (1,'ada'),(2, 'bob');
update `delimiter` set `delimiter`.name='cici' where `delimiter`.id=2;
select * from `delimiter`;
drop table if exists delimiter_test;