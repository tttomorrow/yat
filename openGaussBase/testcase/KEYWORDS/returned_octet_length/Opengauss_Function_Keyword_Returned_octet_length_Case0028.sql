-- @testpoint: opengauss关键字returned_octet_length(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists returned_octet_length_test;
create table returned_octet_length_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists returned_octet_length;
create synonym returned_octet_length for returned_octet_length_test;
insert into returned_octet_length values (1,'ada'),(2, 'bob');
update returned_octet_length set returned_octet_length.name='cici' where returned_octet_length.id=2;
select * from returned_octet_length;
drop synonym if exists returned_octet_length;

--关键字带双引号-成功
drop synonym if exists "returned_octet_length";
create synonym "returned_octet_length" for returned_octet_length_test;
insert into "returned_octet_length" values (1,'ada'),(2, 'bob');
update "returned_octet_length" set "returned_octet_length".name='cici' where "returned_octet_length".id=2;
select * from "returned_octet_length";
drop synonym if exists "returned_octet_length";

--关键字带单引号-合理报错
drop synonym if exists 'returned_octet_length';

--关键字带反引号-合理报错
drop synonym if exists `returned_octet_length`;
drop table if exists returned_octet_length_test;