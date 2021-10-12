-- @testpoint: opengauss关键字dictionary(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists dictionary_test;
create table dictionary_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists dictionary;
create synonym dictionary for dictionary_test;
insert into dictionary values (1,'ada'),(2, 'bob');
update dictionary set dictionary.name='cici' where dictionary.id=2;
select * from dictionary;
drop synonym if exists dictionary;

--关键字带双引号-成功
drop synonym if exists "dictionary";
create synonym "dictionary" for dictionary_test;
drop synonym if exists "dictionary";

--关键字带单引号-合理报错
drop synonym if exists 'dictionary';
create synonym 'dictionary' for dictionary_test;
insert into 'dictionary' values (1,'ada'),(2, 'bob');
update 'dictionary' set 'dictionary'.name='cici' where 'dictionary'.id=2;
select * from 'dictionary';

--关键字带反引号-合理报错
drop synonym if exists `dictionary`;
create synonym `dictionary` for dictionary_test;
insert into `dictionary` values (1,'ada'),(2, 'bob');
update `dictionary` set `dictionary`.name='cici' where `dictionary`.id=2;
select * from `dictionary`;
drop table if exists dictionary_test;