-- @testpoint: opengauss关键字document(非保留)，作为游标名，部分测试点合理报错

--前置条件
drop table if exists document_test cascade;
create table document_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor document for select * from document_test order by 1;
close document;
end;

--关键字带双引号-成功
start transaction;
cursor "document" for select * from document_test order by 1;
close "document";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'document' for select * from document_test order by 1;
close 'document';
end;

--关键字带反引号-合理报错
start transaction;
cursor `document` for select * from document_test order by 1;
close `document`;
end;
drop table if exists document_test cascade;