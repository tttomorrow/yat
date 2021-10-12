-- @testpoint: 和update拼接函数sqrt()
drop table if exists stud_blob;
create table stud_blob(c_id int,b_blob text);
insert into stud_blob values(1,'35466');
commit;
update stud_blob set b_blob= cast(b_blob || sqrt(4) as blob) where c_id=1;
select * from stud_blob where c_id=1 ;
drop table if exists stud_blob;