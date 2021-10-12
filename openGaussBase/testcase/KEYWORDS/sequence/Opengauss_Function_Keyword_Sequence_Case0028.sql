-- @testpoint: opengauss关键字sequence(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists sequence;
create synonym sequence for explain_test;
insert into sequence values (1,'ada'),(2, 'bob');
update sequence set sequence.name='cici' where sequence.id=2;
select * from sequence;
drop synonym if exists sequence;

--关键字带双引号-成功
drop synonym if exists "sequence";
create synonym "sequence" for explain_test;
drop synonym if exists "sequence";

--关键字带单引号-合理报错
drop synonym if exists 'sequence';
create synonym 'sequence' for explain_test;
insert into 'sequence' values (1,'ada'),(2, 'bob');
update 'sequence' set 'sequence'.name='cici' where 'sequence'.id=2;
select * from 'sequence';

--关键字带反引号-合理报错
drop synonym if exists `sequence`;
create synonym `sequence` for explain_test;
insert into `sequence` values (1,'ada'),(2, 'bob');
update `sequence` set `sequence`.name='cici' where `sequence`.id=2;
select * from `sequence`;
drop table if exists explain_test;