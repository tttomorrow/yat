-- @testpoint: DQL语句，结合case when


drop table if exists join_001;

create  table join_001(id int,sales int not null,store_name varchar(100) not null,c_date date);

insert into join_001 values(1,100,'天空a',date '2020-12-10');
insert into join_001 values(2,200,'天空b',date '2020-12-11');
insert into join_001 values(3,500,'天空c',date '2020-12-12');
insert into join_001 values(4,1000,'天空d',date '2020-12-13');
insert into join_001 values(5,3000,'天空e',date '2020-12-14');

select store_name,c_date,case when sales>=1000 then 'Good Day' when sales>=500 then 'OK Day' else 'Bad Day' end from join_001;

drop table join_001;