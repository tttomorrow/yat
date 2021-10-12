drop table if exists tbl_base;

create table tbl_base(
    id int,
    name varchar(128),
    xa timestamp,
    beep varchar(128) null,
    txt clob,
    bin blob
);

drop table if exists trigger_tbl;

create table trigger_tbl(
    id int,
    name varchar(128)
);

create unique index index_id on tbl_base(id);

comment on table tbl_base is 'the base table';
comment on column tbl_base.id 'the primary id of base table'

create or replace trigger tbl_base_trigger after insert on tbl_base for each row

begin
    insert into trigger_tbl values(:new.id, :new.name);
end;
/

insert into table tbl_base values
    (1, 'Javen', '2019-1-1 23:44:55', 'Don not repeat yourself', 'xml/gcc/abc/ddd/xml', 'AB234234FE3423CBB4A'),
    (2, 'Poul', '2010-1-1 23:44:55', 'Don not repeat yourself', 'xml/gcc/abc/ddd/xml', 'AB234234CBB4A'),
    (3, 'Alice', '2049-1-1 23:44:55', 'Don not repeat yourself', 'xml/gcc/abc/ddd/xml', 'AB23343434FE3423CBB4A'),
    (4, 'Jack', '2019-3-1 23:44:55', 'Don not repeat yourself', 'xml/gcc/abc/ddd/xml', 'A3333333423CBB4A');

select * from tbl_base;

select * from trigger_tbl;
