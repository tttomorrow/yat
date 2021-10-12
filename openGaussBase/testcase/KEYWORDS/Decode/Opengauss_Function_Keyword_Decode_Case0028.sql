-- @testpoint: opengauss关键字decode(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists decode_test;
create table decode_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists decode;
create synonym decode for decode_test;
insert into decode values (1,'ada'),(2, 'bob');
update decode set decode.name='cici' where decode.id=2;
select * from decode;
drop synonym if exists decode;

--关键字带双引号-成功
drop synonym if exists "decode";
create synonym "decode" for decode_test;
drop synonym if exists "decode";

--关键字带单引号-合理报错
drop synonym if exists 'decode';
create synonym 'decode' for decode_test;
insert into 'decode' values (1,'ada'),(2, 'bob');
update 'decode' set 'decode'.name='cici' where 'decode'.id=2;
select * from 'decode';

--关键字带反引号-合理报错
drop synonym if exists `decode`;
create synonym `decode` for decode_test;
insert into `decode` values (1,'ada'),(2, 'bob');
update `decode` set `decode`.name='cici' where `decode`.id=2;
select * from `decode`;
drop table if exists decode_test;