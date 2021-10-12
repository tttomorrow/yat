-- @testpoint: opengauss关键字parser(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists parser_test;
create table parser_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists parser;
create synonym parser for parser_test;
insert into parser values (1,'ada'),(2, 'bob');
update parser set parser.name='cici' where parser.id=2;
select * from parser;

--关键字带双引号-成功
drop synonym if exists "parser";
create synonym "parser" for parser_test;


--关键字带单引号-合理报错
drop synonym if exists 'parser';
create synonym 'parser' for parser_test;
insert into 'parser' values (1,'ada'),(2, 'bob');
update 'parser' set 'parser'.name='cici' where 'parser'.id=2;
select * from 'parser';

--关键字带反引号-合理报错
drop synonym if exists `parser`;
create synonym `parser` for parser_test;
insert into `parser` values (1,'ada'),(2, 'bob');
update `parser` set `parser`.name='cici' where `parser`.id=2;
select * from `parser`;
--清理环境
drop synonym if exists "parser";
drop synonym if exists parser;
drop table if exists parser_test;