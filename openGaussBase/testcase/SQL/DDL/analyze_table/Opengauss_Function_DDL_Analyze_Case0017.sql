-- @testpoint:  每组多列统计信息最多支持32列

drop table if exists t1;
create  table t1(id1 int,id2 int,id3 int,id4 int,id5 int,id6 int,id7 int,id8 int,id9 int,id10 int,id11 int,id12 int,id13 int,id14 int,id15 int,id16 int,id17 int,id18 int,id19 int,id20 int,id21 int,id22 int,id23 int,id24 int,id25 int,id26 int,id27 int,id28 int,id29 int,id30 int,id31 int,id32 int);
insert into t1 values(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32);
analyze  t1((id1,id2,id3,id4,id5,id6,id7,id8,id9,id10,id11,id12,id13,id14,id15,id16,id17,id18,id19,id20,id21,id22,id23,id24,id25,id26,id27,id28,id29,id30,id31,id32));
analyze  t1;
drop table if exists t1;