--  @testpoint:opengauss关键字blob(非保留)，作为游标名
--前置条件
drop table if exists blob_test cascade;
create table blob_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor blob for select * from blob_test order by 1;
close blob;
end;

--关键字带双引号-成功
start transaction;
cursor "blob" for select * from blob_test order by 1;
close "blob";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'blob' for select * from blob_test order by 1;
close 'blob';
end;

--关键字带反引号-合理报错
start transaction;
cursor `blob` for select * from blob_test order by 1;
close `blob`;
end;

--清理环境
drop table blob_test;