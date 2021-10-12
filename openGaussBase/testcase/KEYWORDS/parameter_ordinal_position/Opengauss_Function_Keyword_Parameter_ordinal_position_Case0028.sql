-- @testpoint: opengauss关键字parameter_ordinal_position(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists parameter_ordinal_position;
create synonym parameter_ordinal_position for explain_test;
insert into parameter_ordinal_position values (1,'ada'),(2, 'bob');
update parameter_ordinal_position set parameter_ordinal_position.name='cici' where parameter_ordinal_position.id=2;
select * from parameter_ordinal_position;

--关键字带双引号-成功
drop synonym if exists "parameter_ordinal_position";
create synonym "parameter_ordinal_position" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'parameter_ordinal_position';
create synonym 'parameter_ordinal_position' for explain_test;
insert into 'parameter_ordinal_position' values (1,'ada'),(2, 'bob');
update 'parameter_ordinal_position' set 'parameter_ordinal_position'.name='cici' where 'parameter_ordinal_position'.id=2;
select * from 'parameter_ordinal_position';

--关键字带反引号-合理报错
drop synonym if exists `parameter_ordinal_position`;
create synonym `parameter_ordinal_position` for explain_test;
insert into `parameter_ordinal_position` values (1,'ada'),(2, 'bob');
update `parameter_ordinal_position` set `parameter_ordinal_position`.name='cici' where `parameter_ordinal_position`.id=2;
select * from `parameter_ordinal_position`;
--清理环境
drop synonym if exists "parameter_ordinal_position";
drop synonym if exists parameter_ordinal_position;
drop table if exists explain_test;