-- @testpoint: opengauss关键字returned_octet_length(非保留)，作为游标名，部分测试点合理报错

--前置条件
drop table if exists returned_octet_length_test cascade;
create table returned_octet_length_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor returned_octet_length for select * from returned_octet_length_test order by 1;
close returned_octet_length;
end;

--关键字带双引号-成功
start transaction;
cursor "returned_octet_length" for select * from returned_octet_length_test order by 1;
close "returned_octet_length";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'returned_octet_length' for select * from returned_octet_length_test order by 1;
close 'returned_octet_length';
end;

--关键字带反引号-合理报错
start transaction;
cursor `returned_octet_length` for select * from returned_octet_length_test order by 1;
close `returned_octet_length`;
end;
drop table if exists returned_octet_length_test cascade;