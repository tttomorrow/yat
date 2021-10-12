-- @testpoint: opengauss关键字encoding(非保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists encoding_test;
create table encoding_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists encoding;
create synonym encoding for encoding_test;
insert into encoding values (1,'ada'),(2, 'bob');
update encoding set encoding.name='cici' where encoding.id=2;
select * from encoding;
drop synonym if exists encoding;

--关键字带双引号-成功
drop synonym if exists "encoding";
create synonym "encoding" for encoding_test;
drop synonym if exists "encoding";

--关键字带单引号-合理报错
drop synonym if exists 'encoding';
create synonym 'encoding' for encoding_test;
insert into 'encoding' values (1,'ada'),(2, 'bob');
update 'encoding' set 'encoding'.name='cici' where 'encoding'.id=2;
select * from 'encoding';

--关键字带反引号-合理报错
drop synonym if exists `encoding`;
create synonym `encoding` for encoding_test;
insert into `encoding` values (1,'ada'),(2, 'bob');
update `encoding` set `encoding`.name='cici' where `encoding`.id=2;
select * from `encoding`;
drop table if exists encoding_test;