-- @testpoint: DQL语法，混合join查询where连接and

drop table if exists join_001;
drop table if exists join_002;
drop table if exists join_003;

create  table join_001(id int,c_int int not null,c_varchar varchar(100) not null,c_varchar1 varchar(100),c_varchar2 varchar(100),c_date date);
create  table join_002(id int,c_int int not null,c_varchar varchar(100) not null,c_varchar1 varchar(100),c_varchar2 varchar(100),c_date date);
create  table join_003(id int,c_int int not null,c_varchar varchar(100) not null,c_varchar1 varchar(100),c_varchar2 varchar(100),c_date date);

insert into join_001 values(1,1000,'abc123','天空','彩虹',to_timestamp(to_char('1800-01-01 10:51:47'),'yyyy-mm-dd hh24:mi:ss'));
insert into join_001 values(2,2000,'abc123','天空','彩虹',to_timestamp(to_char('1800-01-01 10:51:47'),'yyyy-mm-dd hh24:mi:ss'));
insert into join_001 values(3,3000,'abc123','天空','彩虹',to_timestamp(to_char('1800-01-01 10:51:47'),'yyyy-mm-dd hh24:mi:ss'));
insert into join_001 values(4,4000,'abc123','天空','彩虹',to_timestamp(to_char('1800-01-01 10:51:47'),'yyyy-mm-dd hh24:mi:ss'));
insert into join_001 values(5,5000,'abc123','天空','彩虹',to_timestamp(to_char('1800-01-01 10:51:47'),'yyyy-mm-dd hh24:mi:ss'));


insert into join_002 values(1,1000,'abc123','天空','彩虹',to_timestamp(to_char('1800-01-01 10:51:47'),'yyyy-mm-dd hh24:mi:ss'));
insert into join_002 values(2,2000,'abc123','天空','彩虹',to_timestamp(to_char('1800-01-01 10:51:47'),'yyyy-mm-dd hh24:mi:ss'));
insert into join_002 values(3,3000,'abc123','天空','彩虹',to_timestamp(to_char('1800-01-01 10:51:47'),'yyyy-mm-dd hh24:mi:ss'));
insert into join_002 values(4,4000,'abc123','天空','彩虹',to_timestamp(to_char('1800-01-01 10:51:47'),'yyyy-mm-dd hh24:mi:ss'));

insert into join_003 values(1,1000,'abc123','天空','彩虹',to_timestamp(to_char('1800-01-01 10:51:47'),'yyyy-mm-dd hh24:mi:ss'));
insert into join_003 values(2,2000,'abc123','天空','彩虹',to_timestamp(to_char('1800-01-01 10:51:47'),'yyyy-mm-dd hh24:mi:ss'));


select distinct a.*, b.* from join_001 a full join join_002 b on a.id = b.id and a.c_int = b.c_int right join join_003 w on a.id = w.id and a.c_int = w.c_int and a.c_varchar1 = w.c_varchar1 where a.id <= 11000 and a.c_varchar1 = b.c_varchar1;

drop table join_001;
drop table join_002;
drop table join_003;