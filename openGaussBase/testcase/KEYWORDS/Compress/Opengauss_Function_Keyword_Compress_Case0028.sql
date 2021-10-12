-- @testpoint: opengauss关键字compress(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists compress_test;
create table compress_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists compress;
create synonym compress for compress_test;
insert into compress values (1,'ada'),(2, 'bob');
update compress set compress.name='cici' where compress.id=2;
select * from compress;
drop synonym if exists compress;
--关键字带双引号-成功
drop synonym if exists "compress";
create synonym "compress" for compress_test;
drop synonym if exists "compress";

--关键字带单引号-合理报错
drop synonym if exists 'compress';
create synonym 'compress' for compress_test;
insert into 'compress' values (1,'ada'),(2, 'bob');
update 'compress' set 'compress'.name='cici' where 'compress'.id=2;
select * from 'compress';

--关键字带反引号-合理报错
drop synonym if exists `compress`;
create synonym `compress` for compress_test;
insert into `compress` values (1,'ada'),(2, 'bob');
update `compress` set `compress`.name='cici' where `compress`.id=2;
select * from `compress`;
drop table if exists compress_test;