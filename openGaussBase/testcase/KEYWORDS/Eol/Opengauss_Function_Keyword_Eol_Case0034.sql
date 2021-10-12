-- @testpoint: opengauss关键字eol(非保留)，作为游标名，部分测试点合理报错

--前置条件
drop table if exists eol_test cascade;
create table eol_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor eol for select * from eol_test order by 1;
close eol;
end;

--关键字带双引号-成功
start transaction;
cursor "eol" for select * from eol_test order by 1;
close "eol";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'eol' for select * from eol_test order by 1;
close 'eol';
end;

--关键字带反引号-合理报错
start transaction;
cursor `eol` for select * from eol_test order by 1;
close `eol`;
end;
drop table if exists eol_test cascade;
