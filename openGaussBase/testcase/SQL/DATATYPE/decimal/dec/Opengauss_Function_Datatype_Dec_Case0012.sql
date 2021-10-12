-- @testpoint: 创建本地行存临时表，精度在合理范围值内，插入数据

drop table if exists dec_12;
create temporary table dec_12 (id dec(4,2)) with (orientation=row, compression=no);
insert into dec_12 values (11.11);
insert into dec_12 values (23.00);
insert into dec_12 values (1.1);
select * from dec_12;
drop table dec_12;