--  @testpoint:opengauss关键字cobol(非保留)，作为游标名
--前置条件
drop table if exists cobol_test cascade;
create table cobol_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor cobol for select * from cobol_test order by 1;
close cobol;
end;

--关键字带双引号-成功
start transaction;
cursor "cobol" for select * from cobol_test order by 1;
close "cobol";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'cobol' for select * from cobol_test order by 1;
close 'cobol';
end;

--关键字带反引号-合理报错
start transaction;
cursor `cobol` for select * from cobol_test order by 1;
close `cobol`;
end;

--清理环境
drop table cobol_test;