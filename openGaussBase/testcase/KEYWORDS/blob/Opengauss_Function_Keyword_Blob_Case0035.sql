-- @testpoint: 和update拼接select中变量为text，合理报错
drop table if exists stud_blob;
create table stud_blob(c_id int,b_blob blob);
insert into stud_blob values(1,'35466');
commit;
update stud_blob set b_blob=cast(b_blob || '@#%^&15252' as blob) where c_id=1;
drop table if exists stud_blob;